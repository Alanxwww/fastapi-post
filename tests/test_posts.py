import pytest
from app import schema
## how to get token
def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert res.status_code == 200

    posts = [schema.PostOut(**post) for post in res.json()]
    # 验证数量一致
    assert len(posts) == len(test_posts)

    # 验证字段值是否匹配（这里假设接口返回的顺序与插入顺序一致）
    for i in range(len(test_posts)):
        assert posts[i].post.title == test_posts[i].title
        assert posts[i].post.content == test_posts[i].content
        assert posts[i].post.owner_id == test_posts[i].owner_id

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_unauthorized_user_get_not_exist(client, test_posts):
    res = client.get(f"/posts/8888")
    assert res.status_code == 404

def test_unauthorized_user_get_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200
    
    post = schema.PostOut(**res.json())
    assert post.post.id == test_posts[0].id
    assert post.post.title == test_posts[0].title
    assert post.post.content == test_posts[0].content

@pytest.mark.parametrize("title, content, published", [
    ("Post 1", "Content for post 1", True),
    ("Second Post", "More content here", False),
    ("Another Post", "Even more content", True),
])
def test_create_post(authorized_client, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts/",
        json={"title": title, "content": content, "published": published}
    )

    assert res.status_code == 201
    created_post = schema.Post(**res.json())

    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published

def test_create_post_default_published_true(authorized_client, test_posts):
    post_data = {"title": "arbitrary", "content": "abc"}
    res = authorized_client.post("/posts/",json=post_data)
    assert res.status_code == 201
    created_post = schema.Post(**res.json())

    assert created_post.title == "arbitrary"
    assert created_post.content == "abc"
    assert created_post.published is True

def test_unauthorized_user_create_post(client, test_posts):
    post_data = {"title": "arbitrary", "content": "abc"}
    res = client.post("/posts/",json=post_data)
    assert res.status_code == 401

def test_unauthorized_delete_post(client, test_posts):
    post_id = test_posts[0].id
    res = client.delete(f"/posts/{post_id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_posts):
    post_id = test_posts[0].id
    res = authorized_client.delete(f"/posts/{post_id}")
    assert res.status_code == 204

def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete("/posts/888888")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    other_user_post = next(p for p in test_posts if p.owner_id != test_user["id"])
    res = authorized_client.delete(f"/posts/{other_user_post.id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    post_id = test_posts[0].id  # 拿第一篇帖子的 id
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "published": True
    }

    res = authorized_client.put(f"/posts/{post_id}", json=data)

    assert res.status_code == 200

    updated_post = schema.Post(**res.json())

    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
    assert updated_post.published is True

def test_update_other_user_post(authorized_client, test_user, test_posts):
    other_post = next(p for p in test_posts if p.owner_id != test_user["id"])

    payload = {
        "title": "should not update",
        "content": "forbidden update",
        "published": True,
    }

    res = authorized_client.put(f"/posts/{other_post.id}", json=payload)
    assert res.status_code == 403

def test_unauthorized_update_post(client, test_posts):
    post_id = test_posts[0].id
    res = client.put(
        f"/posts/{post_id}",
        json={"title": "new title", "content": "new content", "published": True}
    )

    assert res.status_code == 401

def test_update_post_not_exist(authorized_client, test_posts):
    res = authorized_client.put(f"/posts/8888"
                                , json={"title": "new title", "content": "new content", "published": True})
    assert res.status_code == 404