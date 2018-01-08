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
    ('A Ann LoCure', 'female'),
    ('Dr. Erik Nelson', 'male'),
    ('Dr. Mark A. Friedman', 'male'),
    ('Rev. Johnny Healey', 'male'),
    ('john_smith', 'male'),
    ('susie123', 'female'),
])
def test_guess_gender(name, gender):
    assert guess_gender(name) == gender
