from random import uniform, randint
from services import Services
from nose.tools import assert_true, assert_equal, assert_false
import requests

points = set()
json_points = set()
test_dict = dict()
rectangles = list()
json_rectangles = set()


def InsertGet(isControllerTest):
    services = Services()
    size = range(0, 100)
    for i in size:
        x_coor = uniform(-999999.999999, 999999.999999)
        y_coor = uniform(-999999.999999, 999999.999999)
        if (x_coor, y_coor) not in test_dict.values():
            if isControllerTest:
                url_insert = 'http://127.0.0.1:5000/insert'
                response = requests.post(url_insert, json = {'x': x_coor, 'y': y_coor})
                if response.ok:
                    assert_equal(i, response.json()['key'])
            else:
                key = services.insert({'x': x_coor, 'y': y_coor})
                assert_equal(i, key)
            test_dict[i] = (x_coor, y_coor)
    for i in size:
        key = i * 3 % 100
        if isControllerTest:
            url_get = 'http://127.0.0.1:5000/get/' + str(key)
            response = requests.get(url_get)
            if response.ok:
                assert_equal(test_dict[key], (response.json()['x'], response.json()['y']))
        else:
            assert_equal(test_dict[key], services.get(key))


def testInsertGet():
    InsertGet(False)
    InsertGet(True)


def InsertRemove(isControllerTest):
    services = Services()
    size = list(range(0,100))
    for i in size:
        x_coor = uniform(-999999.999999, 999999.999999)
        y_coor = uniform(-999999.999999, 999999.999999)
        if (x_coor, y_coor) not in test_dict.values():
            if isControllerTest:
                url_insert = 'http://127.0.0.1:5000/insert'
                response = requests.post(url_insert, json={'x': x_coor, 'y': y_coor})
                if response.ok:
                    assert_equal(i, response.json()['key'])
            else:
                key = services.insert({'x': x_coor, 'y': y_coor})
                assert_equal(i, key)
            test_dict[i] = (x_coor, y_coor)
    while len(size) > 0:
        key = randint(0,99)
        if key in size:
            if isControllerTest:
                already_removed = False
                url_get = 'http://127.0.0.1:5000/get/' + str(key)
                response = requests.get(url_get)
                if response.ok:
                    assert_equal(test_dict[key], (response.json()['x'], response.json()['y']))
                url_remove = 'http://127.0.0.1:5000/remove/' + str(key)
                response = requests.delete(url_remove)
                assert_true(response.ok)
                response = requests.delete(url_remove)
                if not response.ok:
                    already_removed = True
                assert_true(already_removed)
                size.remove(key)
                test_dict.pop(key)

            else:
                already_removed = False
                assert_equal(test_dict[key], services.get(key))
                services.remove(key)
                try:
                    services.remove(key)
                except KeyError:
                    # global already_removed
                    already_removed = True
                assert_true(already_removed)
                size.remove(key)
                test_dict.pop(key)
    assert_false(len(size))
    assert_false(len(test_dict))


def testInsertRemove():
    InsertRemove(False)
    InsertRemove(True)


def GetRemove(isControllerTest):
    services = Services()
    size = list(range(0,100))
    for i in size:
        x_coor = uniform(-999999.999999, 999999.999999)
        y_coor = uniform(-999999.999999, 999999.999999)
        if (x_coor, y_coor) not in test_dict.values():
            if isControllerTest:
                url_insert = 'http://127.0.0.1:5000/insert'
                response = requests.post(url_insert, json={'x': x_coor, 'y': y_coor})
                if response.ok:
                    assert_equal(i, response.json()['key'])
            else:
                key = services.insert({'x': x_coor, 'y': y_coor})
                assert_equal(i, key)
            test_dict[i] = (x_coor, y_coor)
    while len(size) > 0:
        key = randint(0,99)
        if key in size:
            if isControllerTest:
                already_removed = False
                url_get = 'http://127.0.0.1:5000/get/' + str(key)
                response = requests.get(url_get)
                if response.ok:
                    assert_equal(test_dict[key], (response.json()['x'], response.json()['y']))
                url_remove = 'http://127.0.0.1:5000/remove/' + str(key)
                response = requests.delete(url_remove)
                assert_true(response.ok)
                response = requests.get(url_get)
                if not response.ok:
                    already_removed = True
                assert_true(already_removed)
                size.remove(key)
                test_dict.pop(key)

            else:
                already_removed = False
                assert_equal(test_dict[key], services.get(key))
                services.remove(key)
                try:
                    services.get(key)
                except KeyError:
                    already_removed = True
                assert_true(already_removed)
                size.remove(key)
                test_dict.pop(key)
    assert_false(len(size))
    assert_false(len(test_dict))

def testGetRemove():
    GetRemove(False)
    GetRemove(True)

def Search(isControllerTest):

    services = Services()
    services.remove(services.insert({'x': 0, 'y': 0}))
    assert_false(len(services.pointsDictionary.dict))
    size = list(range(0,10))
    assert_false(len(services.search({'x': -1, 'y': -1, 'width': 2, 'height': 2})))
    for i in size:
        x_coor = uniform(-999999.999999, 999999.999999)
        y_coor = uniform(-999999.999999, 999999.999999)
        if (x_coor, y_coor) not in test_dict.values():
            if isControllerTest :
                url_insert = 'http://127.0.0.1:5000/insert'
                response = requests.post(url_insert, json={'x': x_coor, 'y': y_coor})
                if response.ok:
                    key = response.json()['key']
                    # assert_equal(i, key)
                    test_dict[key] = (x_coor, y_coor)
                url_search = 'http://127.0.0.1:5000/search'
                # exact point
                response = requests.get(url_search, json={'x': x_coor, 'y': y_coor, 'width': 0.0, 'height': 0.0})
                if response.ok:
                    assert_equal(tuple(response.json()['points within rectangle'][0]), (x_coor, y_coor))
                # point is rec's BL
                response = requests.get(url_search, json={'x': x_coor, 'y': y_coor, 'width': 1.0, 'height': 1.0})
                if response.ok:
                    assert_equal(tuple(response.json()['points within rectangle'][0]), (x_coor, y_coor))
                # point is rec's TR
                response = requests.get(url_search,
                                        json={'x': x_coor - 1.0, 'y': y_coor - 1.0, 'width': 1.0, 'height': 1.0})
                if response.ok:
                    assert_equal(tuple(response.json()['points within rectangle'][0]), (x_coor, y_coor))
                # point is rec's BR
                response = requests.get(url_search, json={'x': x_coor - 1.0, 'y': y_coor, 'width': 1.0, 'height': 1.0})
                if response.ok:
                    assert_equal(tuple(response.json()['points within rectangle'][0]), (x_coor, y_coor))
                # point is rec's TL
                response = requests.get(url_search, json={'x': x_coor, 'y': y_coor - 1.0, 'width': 1.0, 'height': 1.0})
                if response.ok:
                    assert_equal(tuple(response.json()['points within rectangle'][0]), (x_coor, y_coor))
                # point is on rec's B
                response = requests.get(url_search, json={'x': x_coor - 0.5, 'y': y_coor, 'width': 1.0, 'height': 1.0})
                if response.ok:
                    assert_equal(tuple(response.json()['points within rectangle'][0]), (x_coor, y_coor))
                # point is on rec's T
                response = requests.get(url_search,
                                        json={'x': x_coor - 0.5, 'y': y_coor - 1.0, 'width': 1.0, 'height': 1.0})
                if response.ok:
                    assert_equal(tuple(response.json()['points within rectangle'][0]), (x_coor, y_coor))
                # point is on rec's L
                response = requests.get(url_search, json={'x': x_coor, 'y': y_coor - 0.5, 'width': 1.0, 'height': 1.0})
                if response.ok:
                    assert_equal(tuple(response.json()['points within rectangle'][0]), (x_coor, y_coor))
                # point is on rec's R
                response = requests.get(url_search,
                                        json={'x': x_coor - 1.0, 'y': y_coor - 0.5, 'width': 1.0, 'height': 1.0})
                if response.ok:
                    assert_equal(tuple(response.json()['points within rectangle'][0]), (x_coor, y_coor))
            else:
                key = services.insert({'x': x_coor, 'y': y_coor})
                test_dict[key] = (x_coor, y_coor)
                # exact point
                list_of_current_point = services.search({'x': x_coor, 'y': y_coor, 'width': 0.0, 'height': 0.0})
                assert_equal(list_of_current_point[0], (x_coor, y_coor))
                # point is rec's BL
                list_of_current_point = services.search({'x': x_coor, 'y': y_coor, 'width': 1.0, 'height': 1.0})
                assert_equal(list_of_current_point[0], (x_coor, y_coor))
                # point is rec's TR
                list_of_current_point = services.search({'x': x_coor-1.0, 'y': y_coor-1.0, 'width': 1.0, 'height': 1.0})
                assert_equal(list_of_current_point[0], (x_coor, y_coor))
                # point is rec's BR
                list_of_current_point = services.search({'x': x_coor-1.0, 'y': y_coor, 'width': 1.0, 'height': 1.0})
                assert_equal(list_of_current_point[0], (x_coor, y_coor))
                # point is rec's TL
                list_of_current_point = services.search({'x': x_coor, 'y': y_coor-1.0, 'width': 1.0, 'height': 1.0})
                assert_equal(list_of_current_point[0], (x_coor, y_coor))
                # point is on rec's B
                list_of_current_point = services.search({'x': x_coor-0.5, 'y': y_coor, 'width': 1.0, 'height': 1.0})
                assert_equal(list_of_current_point[0], (x_coor, y_coor))
                # point is on rec's T
                list_of_current_point = services.search({'x': x_coor-0.5, 'y': y_coor-1.0, 'width': 1.0, 'height': 1.0})
                assert_equal(list_of_current_point[0], (x_coor, y_coor))
                # point is on rec's L
                list_of_current_point = services.search({'x': x_coor, 'y': y_coor-0.5, 'width': 1.0, 'height': 1.0})
                assert_equal(list_of_current_point[0], (x_coor, y_coor))
                # point is on rec's R
                list_of_current_point = services.search({'x': x_coor-1.0, 'y': y_coor-0.5, 'width': 1.0, 'height': 1.0})
                assert_equal(list_of_current_point[0], (x_coor, y_coor))
        if not i%4:
            if isControllerTest:
                key = str(round(i/2))
                url_remove = 'http://127.0.0.1:5000/remove/' + key
                response = requests.delete(url_remove)
                if response.ok:
                    size.remove(i/2)
                    test_dict.pop(i/2)
                else:
                    assert_false(i)
            else:
                try:
                    services.remove(i/2)
                    size.remove(i/2)
                    test_dict.pop(i/2)
                except KeyError:
                    assert_false(i)
            x0 = uniform(-999999.999999, 999999.999999)
            y0 = uniform(-999999.999999, 999999.999999)
            width_size = uniform(0, 1999999.999999999999)
            height_size = uniform(0, 1999999.999999999999)
            if (x0, y0, width_size, height_size) not in rectangles:
                rectangles.append((x0, y0, width_size, height_size))
    for i in range(3):
        if isControllerTest:
            url_search = 'http://127.0.0.1:5000/search'
            response = requests.get(url_search, json={'x': rectangles[i][0], 'y': rectangles[i][1], 'width': rectangles[i][2], 'height': rectangles[i][3]})
            points_in_rectangle = [tuple(point) for point in response.json()['points within rectangle']]
            result_points = [point for point in test_dict.values() if rectangles[i][0]+rectangles[i][2] >= point[0] >= rectangles[i][0] and rectangles[i][1]+rectangles[i][3] >= point[1] >= rectangles[i][1]]
            if response.ok:
                assert_equal(set(result_points), set(points_in_rectangle))
        else:
            points_in_rectangle = services.search({'x': rectangles[i][0], 'y': rectangles[i][1], 'width': rectangles[i][2], 'height': rectangles[i][3]})
            result_points = [point for point in test_dict.values() if rectangles[i][0]+rectangles[i][2] >= point[0] >= rectangles[i][0] and rectangles[i][1]+rectangles[i][3] >= point[1] >= rectangles[i][1]]
            assert_equal(set(points_in_rectangle), set(result_points))

def testSearch():
    Search(False)
    Search(True)

