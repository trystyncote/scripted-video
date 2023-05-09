from src.scripted_video.ImageObject import ImageObject


class ObjectDict(dict):
    def __setitem__(self, key: str, value: ImageObject):
        if not isinstance(key, str):
            raise KeyError("Key must be a string.")
        # if not isinstance(value, ImageObject):
        #     raise ValueError(f"Value is not valid type. Received {type(value)}")
        if key != value.object_name:
            raise KeyError(f"Key name must be identical to object name. {key=} {value.object_name=}")
        super().__setitem__(key, value)
