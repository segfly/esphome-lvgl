import esphome.config_validation as cv
from .defines import CONF_LABEL, CONF_LONG_MODE, LV_LONG_MODES, CONF_TEXT, CONF_RECOLOR
from .lv_validation import lv_bool, lv_text
from .schemas import TEXT_SCHEMA
from .types import lv_label_t
from .widget import Widget, WidgetType


class LabelType(WidgetType):
    def __init__(self):
        super().__init__(
            CONF_LABEL,
            TEXT_SCHEMA.extend(
                {
                    cv.Optional(CONF_RECOLOR): lv_bool,
                    cv.Optional(CONF_LONG_MODE): LV_LONG_MODES.one_of,
                }
            ),
        )

    @property
    def w_type(self):
        return lv_label_t

    async def to_code(self, w: Widget, config):
        """For a text object, create and set text"""
        init = []
        if value := config.get(CONF_TEXT):
            init.extend(w.set_property(CONF_TEXT, await lv_text.process(value)))
        init.extend(w.set_property(CONF_LONG_MODE, config))
        init.extend(w.set_property(CONF_RECOLOR, config))
        return init


label_spec = LabelType()
