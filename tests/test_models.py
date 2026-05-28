from models import User

# ************* One Unit Test (Models / Pure Logic) **************************

def test_user_password_hashing_behaves_correctly():
    user = User(username="test")
    user.set_password(password="testpassword")

    assert user.password_hash is not None
    assert user.check_password(password="testpassword") == True
