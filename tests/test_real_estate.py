import pytest
from app import schemas


# def test_get_real_estate(session, test_real_estate_mainz):
#     res = session.get("/real_estate/")

#     def validate(real_estate):
#         return schemas.RealEstateOut(**real_estate)
#     real_estate_map = map(validate, res.json())
#     real_estates_list = list(real_estate_map)

#     assert len(res.json()) == len(test_real_estates)
#     assert res.status_code == 200


# def test_unauthorized_user_get_all_posts(client, test_posts):
#     res = client.get("/posts/")
#     assert res.status_code == 401


# def test_unauthorized_user_get_one_post(client, test_posts):
#     res = client.get(f"/posts/{test_posts[0].id}")
#     assert res.status_code == 401


def test_get_one_real_estate_not_exist(client, test_real_estate_mainz):
    res = client.get(f"/real_estate/88888")
    assert res.status_code == 404


def test_get_one_real_estate(client, test_real_estate_mainz):
    print(test_real_estate_mainz[0].id)
    res = client.get(f"/real_estate/{test_real_estate_mainz[0].id}")
    real_estate = schemas.RealEstateOut(**res.json())
    assert real_estate.id == test_real_estate_mainz[0].id
    assert real_estate.full_address == test_real_estate_mainz[0].full_address


@pytest.mark.parametrize("geom, full_address, street, house_number, postal_code, city", [  
                        ("POINT(50.000205993652344 8.26205825805664)","Binger Straße 2, 55116 Mainz", "Binger Straße","2","55116", "Mainz"),
                        ("POINT(49.984554 8.249938)","Michael-Müller-Ring 23, 55128 Mainz","Michael-Müller-Ring","23","55128","Mainz"),
                        ( "POINT(49.960860 8.253250)","Carl-Zeiss-Straße 42, 55129 Mainz", "Carl-Zeiss-Straße","42","55129","Mainz")
        ])
def test_create_real_estate(client, geom, full_address, street, house_number, postal_code, city):
    res = client.post(
        "/real_estate/", json={"geom": geom, "full_address": full_address, "street": street, "house_number": house_number, "postal_code": postal_code, "city": city})

    created_real_estate = schemas.RealEstateOut(**res.json())
    assert res.status_code == 201
    assert created_real_estate.full_address == full_address


# def test_unauthorized_user_create_post(client, test_user, test_posts):
#     res = client.post(
#         "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"})
#     assert res.status_code == 401


def test_unauthorized_user_delete_Post(client, test_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


# def test_delete_post_success(authorized_client, test_user, test_posts):
#     res = authorized_client.delete(
#         f"/posts/{test_posts[0].id}")

#     assert res.status_code == 204


# def test_delete_post_non_exist(authorized_client, test_user, test_posts):
#     res = authorized_client.delete(
#         f"/posts/8000000")

#     assert res.status_code == 404


# def test_delete_other_user_post(authorized_client, test_user, test_posts):
#     res = authorized_client.delete(
#         f"/posts/{test_posts[3].id}")
#     assert res.status_code == 403


def test_update_post(client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id

    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


# def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
#     data = {
#         "title": "updated title",
#         "content": "updatd content",
#         "id": test_posts[3].id

#     }
#     res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
#     assert res.status_code == 403


# def test_unauthorized_user_update_post(client, test_user, test_posts):
#     res = client.put(
#         f"/posts/{test_posts[0].id}")
#     assert res.status_code == 401


def test_update_real_estate_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(
        f"/posts/8000000", json=data)

    assert res.status_code == 404