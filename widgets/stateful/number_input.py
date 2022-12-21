from typing import Any, MutableMapping, Optional, Union

import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from streamlit.elements.number_input import Number
from streamlit.runtime.state.session_state import WidgetCallback
from streamlit.runtime.state.widgets import NoValue
from streamlit.type_util import Key

from widgets.stateful import _on_change_factory


def _update_value(session: MutableMapping[Key, Any], key: str):
    session[f"{key}_value"] = session[key]


def stateful_number_input(
    label: str,
    key: str,
    value: Union[NoValue, Number, None] = NoValue(),
    position: DeltaGenerator = st._main,
    session: MutableMapping[Key, Any] = st.session_state,
    on_change: Optional[WidgetCallback] = None,
    **kwargs,
):
    """
    A stateful number input that preserves value.
    """
    if key not in session:
        session[key] = None

    if f"{key}_value" not in session:
        session[f"{key}_value"] = value

    session[key] = position.number_input(
        label,
        value=session[f"{key}_value"],
        key=None,  # NOTE: avoid collisions with session state API
        on_change=_on_change_factory(_update_value, session, key)(on_change),
        **kwargs,
    )
    return session[key]
