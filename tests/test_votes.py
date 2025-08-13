import pytest
from app import models

@pytest.fixture()
def existing_vote(test_posts, test_user, session):
    new_vote = models.Vote(post_id=test_posts[2].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()
    session.refresh(new_vote)
    return new_vote
    

def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/",
        json={"post_id": test_posts[0].id, "dir": 1}  
    )
    assert res.status_code == 201  


def test_vote_twice_post(authorized_client, test_posts, existing_vote):
    res = authorized_client.post(
        "/vote/",
        json={"post_id": test_posts[2].id, "dir": 1}
        )
    assert res.status_code == 409

def test_delete_vote(authorized_client, test_posts, existing_vote):
    res = authorized_client.post(
        "/vote/",
        json={"post_id": test_posts[2].id, "dir": 0}
        )
    assert res.status_code == 201

def test_unlike_vote_not_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/",
        json={"post_id": test_posts[2].id, "dir": 0}
        )
    assert res.status_code == 404

def test_like_vote_not_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/",
        json={"post_id": 88888, "dir": 1}
        )
    assert res.status_code == 404

def test_unauthorized_user_like_vote(client, test_posts):
    res = client.post(
        "/vote/",
        json={"post_id": 88888, "dir": 1}
        )
    assert res.status_code == 401