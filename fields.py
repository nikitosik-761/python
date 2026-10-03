import json
import re
import os
import uuid
from datetime import datetime
from datetime import date


class Field:

    def __init__(self, nullable=False):
        self.nullable = nullable

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.private_name, None)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.private_name, value)

    def __delete__(self, instance):
        delattr(instance, self.private_name)

    def validate(self, value):
        if value is None:
            if not self.nullable:
                raise ValueError(f"Поле {self.private_name} не может быть null")
            return
        self._validate(value)

    def _validate(self, value):
        pass

    def to_python(self, value):
        return value

    def to_json(self, value):
        return value


class StringField(Field):

    def __init__(self, min_length=0, max_length=255, regex=None, nullable=False):
        super().__init__(nullable)
        self.min_length = min_length
        self.max_length = max_length
        self.regex = re.compile(regex) if regex else None

    def _validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Поле {self.public_name} не соответствует типу str")

        if not (self.min_length <= len(value) <= self.max_length):
            raise ValueError(
                f"Поле {self.public_name} должно находиться в диапазоне от {self.min_length} до {self.max_length}")

        if self.regex and not self.regex.fullmatch(value):
            raise ValueError(f"Поле {self.public_name}: Значение {value} не соответствует шаблону {self.regex.pattern}")


class IntegerField(Field):

    def __init__(self, min_value=None, max_value=None, nullable=False):
        super().__init__(nullable)
        self.min_value = min_value
        self.max_value = max_value

    def _validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Поле {self.public_name} должно быть типом int")
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Поле {self.public_name} не может быть меньше {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Поле {self.public_name} не может быть больше {self.max_value}")


class EmailField(StringField):
    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    def __init__(self, nullable=False):
        super().__init__(min_length=5, max_length=255, regex=EmailField.EMAIL_REGEX, nullable=nullable)


class DateField(Field):
    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, nullable=False):
        super().__init__(nullable)

    def __set__(self, instance, value):
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, DateField.DATE_FORMAT).date()
            except ValueError:
                raise ValueError(f"Поле {self.public_name}: '{value}' не соответствует формату {DateField.DATE_FORMAT}")
        super().__set__(instance, value)

    def _validate(self, value):
        if isinstance(value, datetime):
            value = value.date()
        if not isinstance(value, date):
            raise TypeError(f"Поле {self.public_name} должно быть date")

    def to_json(self, value):
        return value.strftime(DateField.DATE_FORMAT) if value else None

    def to_python(self, value):
        if isinstance(value, str):
            return datetime.strptime(value, DateField.DATE_FORMAT).date()

        return value


class ModelMeta(type):

    def __new__(cls, name, bases, namespaces):
        fields = {}
        for base in bases:
            if hasattr(base, "_fields"):
                fields.update(base._fields)

        for attr_name, attr_value in namespaces.items():
            if isinstance(attr_value, Field):
                fields[attr_name] = attr_value

        custom_class = super().__new__(cls, name, bases, namespaces)

        custom_class._fields = fields

        if fields:
            custom_class.__init__ = cls._make_init(fields)
            custom_class.__repr__ = cls._make_repr(name, fields)
            custom_class.to_dict = cls._make_to_dict(fields)
            custom_class.from_dict = classmethod(cls._make_from_dict(fields))

        return custom_class

    @staticmethod
    def _make_init(fields):
        field_names = list(fields.keys())

        def __init__(self, **kwargs):
            for key in kwargs:
                if key not in field_names:
                    raise TypeError(f"Неизвестное поле: {key}")
            for field_name in field_names:
                if field_name in kwargs:
                    setattr(self, field_name, kwargs[field_name])
                elif fields[field_name].nullable:
                    setattr(self, field_name, None)

        return __init__

    @staticmethod
    def _make_repr(class_name, fields):
        def __repr__(self):
            parts = [f"{field_name}={getattr(self, field_name, None)}" for field_name in fields]
            return f"{class_name}({", ".join(parts)})"

        return __repr__

    @staticmethod
    def _make_to_dict(fields):
        def to_dict(self):
            return {field_name: descriptor.to_json(getattr(self, field_name, None)) for field_name, descriptor in fields.items()}

        return to_dict

    @staticmethod
    def _make_from_dict(fields):
        def from_dict(cls, data):
            obj = cls.__new__(cls)
            for field_name, descriptor in fields.items():
                raw = data.get(field_name)
                value = descriptor.to_python(raw)
                setattr(obj, field_name, value)
            return obj

        return from_dict


class Model(metaclass=ModelMeta):
    FILE_NAME = "db.json"
    ID = StringField(nullable=False)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.ID == other.ID

    def __hash__(self):
        return hash((type(self).__name__, self.ID))

    def validate(self):
        for field_name, descriptor in self._fields.items():
            descriptor.validate(getattr(self, field_name, None))

    @classmethod
    def _read_all(cls):
        if not os.path.exists(cls.FILE_NAME):
            raise ValueError("Путь не существует")
        with open(cls.FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data.get(cls.__name__, [])

    @classmethod
    def _write_all(cls, entities):
        if not os.path.exists(cls.FILE_NAME):
            raise ValueError("Путь не существует")

        all_data = {}

        with open(cls.FILE_NAME, "r", encoding="utf-8") as file:
            all_data = json.load(file)

        all_data[cls.__name__] = entities

        with open(cls.FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(all_data, file, ensure_ascii=False, indent=4)

    def save(self):
        self.validate()
        entities = self._read_all()
        data = self.to_dict(self)

        new_id = str(uuid.uuid4())
        data["id"] = new_id
        self.ID = new_id

        entities.append(data)

        self._write_all(entities)
        print("Сохранение успешно выполнено")

    @classmethod
    def load(cls, id_):
        for rec in cls._read_all():
            if rec.get("id") == id_:
                return cls.from_dict(rec)
        return None

    @classmethod
    def all(cls):
        return [cls.from_dict(rec) for rec in cls._read_all()]

    @classmethod
    def filter(cls, **kwargs):
        return [
            cls.from_dict(rec)
            for rec in cls._read_all()
            if all(rec.get(k) == v for k, v in kwargs.items())
        ]

    @classmethod
    def delete(cls, id_):
        records = cls._read_all()
        new_records = [r for r in records if r.get("id") != id_]
        if len(new_records) == len(records):
            return False
        cls._write_all(new_records)
        return True
