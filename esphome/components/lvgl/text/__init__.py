import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text

from .. import add_init_lambda, LVGL_SCHEMA, Widget
from ..defines import CONF_WIDGET, CONF_LVGL_ID
from ..lv_validation import requires_component
from ..types import lvgl_ns, LvText
from ..widget import get_widget

LVGLText = lvgl_ns.class_("LVGLText", text.Text)

CONFIG_SCHEMA = cv.All(
    text.TEXT_SCHEMA.extend(LVGL_SCHEMA).extend(
        {
            cv.GenerateID(): cv.declare_id(LVGLText),
            cv.Required(CONF_WIDGET): cv.use_id(LvText),
        }
    ),
    requires_component("text"),
)


async def to_code(config):
    var = await text.new_text(config)
    paren = await cg.get_variable(config[CONF_LVGL_ID])
    widget = await get_widget(config[CONF_WIDGET])
    assert isinstance(widget, Widget)
    value = widget.get_value()
    publish = f"{var}->publish_state({value})"
    init = widget.set_event_cb(publish, "LV_EVENT_VALUE_CHANGED")
    init.append(f"{var}->set_control_lambda([] (std::string text) {{")
    init.extend(widget.set_property("text", "text.c_str()"))
    init.extend(
        [
            f"""
               lv_event_send({widget.obj}, {paren}->get_custom_change_event(), nullptr);
               {publish};
            }})""",
            publish,
        ]
    )
    await add_init_lambda(paren, init)
