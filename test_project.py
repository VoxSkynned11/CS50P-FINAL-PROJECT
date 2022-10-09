import pytest
import PIL
import pathlib
from project import *



def test_StreamsId():
    id = StreamsId()
    id.m_items.append(1)
    id.m_id['item'] = 1
    assert id.check() == 0

    id = StreamsId()
    id.m_items.append(1)
    id.m_items.append(2)
    id.m_id['item'] = 1
    with pytest.raises(ValueError):
        id.check()

def test_main():
    # if exit is chosen
    assert main() == 0

