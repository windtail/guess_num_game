# coding: utf-8

import streamlit as st
from random import randint
from dataclasses import dataclass, field


def new_number() -> int:
    return randint(1, 100)


@dataclass
class State:
    name: str = "init"

    num: int = field(default_factory=new_number)
    """
    待猜的数字
    """

    guess: int = 1
    """
    用户上一次猜的数字
    """

    times: int = 0
    """
    猜的次数
    """


if "state" not in st.session_state:
    st.session_state["state"] = State()

state = st.session_state["state"]

def set_state(new_state: State):
    st.session_state["state"] = new_state
    st.rerun()


st.set_page_config(page_title="猜数字")

st.header("猜数字 1~100", divider="gray")

if state.name == "init":
    if st.button("点击开始"):
        set_state(State("first-guess"))
elif state.name == "first-guess":
    num = st.number_input("猜猜我想的是什么数字", min_value=1, max_value=100, step=1, value=state.guess)
    if st.button("我猜"):
        state.times += 1
        if num == state.num:
            state.name = "correct"
            set_state(state)
        else:
            state.name = "guess"
            state.guess = num
            set_state(state)
elif state.name == "guess":
    if state.guess > state.num:
        msg = "太大了"
    else:
        msg = "太小了"

    num = st.number_input(f"{msg}, 你已经猜错了{state.times}次", min_value=1, max_value=100, step=1, value=state.guess)
    if st.button("我猜"):
        state.times += 1
        if num == state.num:
            state.name = "correct"
            set_state(state)
        else:
            state.guess = num
            set_state(state)
    if st.button("重新开始"):
        set_state(State("first-guess"))
else:
    if state.times == 1:
        msg = "你太幸运了！"
    elif state.times <= 7:
        msg = "干得不错！"
    elif state.times < 10:
        msg = "二分法没有掌握好"
    else:
        msg = "猜得不太好，下次再努力"
    st.text(f"猜对了，数字是{state.num}。你猜了{state.times}次，{msg}")
    if st.button("重新开始"):
        set_state(State("first-guess"))
