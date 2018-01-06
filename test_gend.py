import pytest

from gend import guess_gender

@pytest.mark.parametrize("name, gender", [
    ('Ned', 'male'),
    ('Susan', 'female'),
    ('SusanS', 'female'),
    ('mary-foobar', 'female'),
    ('Chin (Maxine) Yang', 'female'),
    ('J. Robert Smith', 'male'),
    ('Dr. John Smith', 'male'),
    ('Ms. Foobar baz', 'female'),
])
def test_guess_gender(name, gender):
    assert guess_gender(name) == gender
