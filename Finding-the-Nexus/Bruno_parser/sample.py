# -*- coding: utf-8 -*-
import os
import sys
import shutil
import subprocess
import traceback
import time
import requests
from pprint import pprint

# выключить предупреждение
requests.packages.urllib3.disable_warnings()
# -----------------------------------------------------------
def find_scenes_in_DB(FC_in_GDB, field_names_list = ['ID', 'ARCHIVE']):
    with arcpy.da.SearchCursor(FC_in_GDB, field_names_list) as DB_cursor:
        uniq_sat_name = sorted({row[0] for row in DB_cursor})
        DB_cursor.reset()
        uniq_sat_archive = sorted({row[1] for row in DB_cursor})
    uniq_sat_name += uniq_sat_archive  
    return uniq_sat_name
# -----------------------------------------------------------
# замеры времени
def Time_now():
    return time.time()
# -----------------------------------------------------------
def Time_elapsed(time_start, time_end):
    return time_end - time_start
# ---------------------------s--------------------------------
# сгенерировать текст запроса (URL) и вернуть его в виде текста

def generate_json_request(
        request_code,
        json_request_content,
        http_service_endpoint=r'https://earthexplorer.usgs.gov/inventory/json/v/1.4.0/'
):
    return str(http_service_endpoint + request_code + r'?jsonRequest=' + json_request_content)
# -----------------------------------------------------------
# авторизироваться на сайте и получить токен доступа
def login(username, password, catalogId, authType = 'EROS'):
    URL = generate_json_request(
        request_code='login',
        json_request_content='{' +
        '"username":"'    + username  +
        '","password":"'  + password  +
        '","authType":"'  + authType  + 
        '","catalogId":"' + catalogId +
        '"}'
    )

    # послать POST запрос
    answer = requests.post(URL)

    # проверка прошёл ли запрос
    check_answer = (answer.status_code, answer.reason)

    if check_answer != (200, 'OK'):
        print u'Ошибка! Сайт не доступен.', check_answer, u'Ссылка:'
        print URL[:150], '...'
        return None

    else:
        # если ошибка (авторизация провалена)
        if answer.json()['errorCode'] is not None:
            print u'Ошибка!', answer.json()['errorCode'] + ':', answer.json()['error']

            # else:
            #     print u'Авторизация успешна! Токен:', answer.json()['data']
        return answer.json()['data']

# удалить токен авторизации
def logout(apiKey):
    if apiKey is not None:

        URL = generate_json_request(
            request_code='logout',
            json_request_content='{"apiKey":"' + apiKey + '"}'
        )

        # послать POST запрос
        answer = requests.post(URL)

        # проверка прошёл ли запрос
        check_answer = (answer.status_code, answer.reason)

        if check_answer != (200, 'OK'):
            print u'Ошибка! Сайт не доступен.', check_answer, u'Ссылка:'
            print URL[:150], '...'

        else:
            # если ошибка
            if answer.json()['errorCode'] is not None:
                #            print u'Ошибка!', answer.json()['errorCode'] + ':', answer.json()['error']
                return None

            else:
                #            if  answer.json()['data'] == False:
                #                print u'Токен НЕ удалён.'
                #                pprint(answer.json())
                #            else:
                #                print u'Токен удалён.'
                return answer.json()['data']

def datasetfields(datasetName, apiKey, node='EE'):
    URL = generate_json_request(
        request_code='datasetfields',
        json_request_content='{"apiKey":"' + apiKey + '", "node": "' + node + '", "datasetName": "' + datasetName + '"}'
    )

    # послать POST запрос
    answer = requests.post(URL)

    # проверка прошёл ли запрос
    check_answer = (answer.status_code, answer.reason)

    if check_answer != (200, 'OK'):
        print u'Ошибка! Сайт не доступен.', check_answer, u'Ссылка:'
        print URL[:150], '...'

    else:
        # если ошибка
        if answer.json()['errorCode'] is not None:
            print u'Ошибка!', answer.json()['errorCode'] + ':', answer.json()['error']
            return None
        else:
            return answer.json()

# сформировать критерий поиска снимков на основе списка Path Row
def additionalCriteria(list_Path_Row, datasetName):
    additionalCriteria = '{"filterType":"or", "childFilters":['
    # первая итерация?
    first_time = True

    for x in datasetfields(datasetName, apiKey).get('data'):
        if x.get('name') == 'WRS Path': Path_fieldId = x.get('fieldId')
        if x.get('name') == 'WRS Row':   Row_fieldId = x.get('fieldId')

    for PR in list_Path_Row:
        Path = str(PR[0])
        Row = str(PR[1])

        filter_Path = '{"filterType":"value", "fieldId":' + str(Path_fieldId) + ', "value":"' + Path + '", "operand":"="}'  # "fieldId":10036 - PATH
        filter_Row = '{"filterType":"value", "fieldId":' + str(Row_fieldId) + ', "value":"' + Row + '", "operand":"="}'  # "fieldId":10038 - ROW
        filter_And = '{"filterType":"and", "childFilters":[' + filter_Path + ',' + filter_Row + ']}'

        # если первая - не добавляем запятую в начало
        if first_time == True:
            additionalCriteria += filter_And
            first_time = False
        else:
            additionalCriteria += ' ,' + filter_And

    additionalCriteria += ']}'
    return additionalCriteria

# поиск снимков
def search_scenes(datasetName, list_Path_Row, apiKey,
                  startDate='2016-05-01T00:00:00Z',
                  endDate='2100-01-01T00:00:00Z',
                  months=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                  maxResults=10,
                  ):
    URL = generate_json_request(
        request_code='search',
        json_request_content='{"datasetName":"' + datasetName + '"' + \
                             ',"temporalFilter":{"dateField": "search_date","startDate":"' + startDate + '","endDate":"' + endDate + '"}' + \
                             ',"months":' + str(months) + \
                             ',"maxResults":' + str(maxResults) + \
                             ',"additionalCriteria":' + additionalCriteria(list_Path_Row, datasetName) + \
                             ',"node":"EE","apiKey":"' + apiKey + '"}'
    )

    # послать POST запрос
    answer = requests.post(URL)

    # проверка прошёл ли запрос
    check_answer = (answer.status_code, answer.reason)

    if check_answer != (200, 'OK'):
        print u'Ошибка! Сайт не доступен.', check_answer, u'Ссылка:'
        print URL[:150], '...'
        print
        print URL

    else:
        # если ошибка
        if answer.json()['errorCode'] is not None:
            print u'Ошибка!', answer.json()['errorCode'] + ':', answer.json()['error']
            return None
        else:
            if answer.json()['data'] in (None, ''):
                print u'Снимков не найдено.'
            else:
                number_of_scenes = answer.json()['data']['totalHits']

            dwnld_URL_list = []
            for scene in answer.json()['data']['results']:
                dwnld_URL_list.append(scene['entityId'])

            return dwnld_URL_list

# вернуть список URL для прямой закачки снимков
def get_download_list(datasetName, entityIds, apiKey, node='EE', products='["STANDARD"]'):
    entityIds = str(['"' + x.encode('UTF8') + '"' for x in entityIds]).replace("'", '')

    URL = generate_json_request(
        request_code='download',
        json_request_content='{' + \
                             '"datasetName": "' + datasetName + '",' + \
                             '"apiKey": "' + apiKey + '",' + \
                             '"node": "' + node + '",' + \
                             '"entityIds": ' + str(entityIds) + ',' + \
                             '"products": ' + products + \
                             '}'
    )

    # послать POST запрос
    answer = requests.post(URL)

    # проверка прошёл ли запрос
    check_answer = (answer.status_code, answer.reason)

    if check_answer != (200, 'OK'):
        print u'Ошибка! Сайт не доступен.', check_answer, u'Ссылка:'
        print URL[:150], '...'
        return None

    else:
        # если ошибка (авторизация провалена)
        if answer.json()['errorCode'] is not None:
            print u'Ошибка!', answer.json()['errorCode'] + ':', answer.json()['error']
        return answer.json()['data']

# делаем список уже закаченных файлов
def list_of_scenes_in_archive(archive_path):
    # archive_path = archive_path.decode('utf-8')
    loaded = []
    dirList = os.listdir(archive_path)
    for fname in dirList:
        fname = fname[:fname.rfind('.')]  # удаляются 4 последних знака (в моём случае это ".rar")
        loaded.append(fname)
    return loaded

# скачать и сохранить файл
def download_file(url, file_path):
    r = requests.get(url, timeout=120, stream=True)
    with open(file_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)
    return file_path

# тестировать файл формата tar.gz
def test_gz_archive(archive_path, GZIP_path):
    coding = 'cp1251'
    GZIP_path = GZIP_path.encode(coding)
    archive_path = archive_path.encode(coding)
    cmd_list = [GZIP_path, '-t', archive_path]
    # запуск консоли и выполнение команды в скрытном режиме с выводом
    subprocess.check_output(cmd_list, stderr=subprocess.STDOUT, shell=True)

def main(username, password, catalogId, datasets, WRS_2_Path_Row_list, WRS_1_Path_Row_list, archive_path, temp_dwnld_folder, FC_in_GDB):
    while True:

        try:
            print time.strftime("%d.%m.%Y %H:%M:%S"),
            global apiKey  # глобальная переменная!!!
            apiKey = login(username, password, catalogId)  # авторизация

            # список уже закаченных снимков
            loaded = list_of_scenes_in_archive(archive_path)
            print u"Всего файлов в локальном хранилище:", len(loaded)

            loaded_2 = find_scenes_in_DB(FC_in_GDB)
            loaded += loaded_2

            for dataset in datasets:
                # print '---------------------------'
                print u'Набор данных:', dataset

                if dataset in 'LANDSAT_MSS':
                    list_Path_Row = WRS_1_Path_Row_list
                else:
                    list_Path_Row = WRS_2_Path_Row_list

                # делаем запросы на каждый отдельный Path-Row, чтобы не превысить ограничение по длине URL
                for path_row in list_Path_Row:

                    entityIds = search_scenes(datasetName=dataset,
                                              list_Path_Row=[path_row],
                                              apiKey=apiKey,
                                              maxResults=50000)

                    # список сцен которых нет в архиве
                    dwnld_list = list(set(entityIds) - set(loaded))

                    if len(dwnld_list) > 0:
                        print time.strftime("%d.%m.%Y %H:%M:%S"),
                        print u'Path Row:', str(path_row[0]), str(path_row[1]) + '.',
                        print u'Всего снимков:', str(len(entityIds)) + '.',
                        print u'Новых:', str(len(dwnld_list)) + '.',
                        print u'Закачка файлов:'

                        # получаем сслыку на закачку для каждой отдельной сцены
                        for (scene_num, dwnld_scene) in enumerate(dwnld_list):

                            DICTs_list = get_download_list(dataset, [dwnld_scene], apiKey, node='EE',
                                                          products='["STANDARD"]')

                            # скачать снимки
                            for DICT in DICTs_list:
                                print time.strftime("%d.%m.%Y %H:%M:%S"), u'Cнимок:',
                                URL = DICT[u'url']

                                # формирование пути
                                scene_product_ID = URL[URL.rfind('/') + 1:URL.rfind('.tar.gz?')]   # название снимка по-новому
                                scene_ID = DICT[u'entityId'] # название снимка по-старому

                                scene_path = os.path.join(temp_dwnld_folder, scene_product_ID + u'.tar.gz')

                                print str(scene_num + 1), scene_product_ID

                                time_start = Time_now()  # текущее время (начало закачки)

                                try:
                                    ##                                    print
                                    ##                                    print '-'*10
                                    ##                                    print URL
                                    ##                                    print scene_path
                                    real_file_len = requests.head(URL).headers[
                                        'content-length']  # размер файла на сервере
                                    download_file(URL, scene_path)  # закачка
                                    dwnld_file_len = str(long(os.path.getsize(scene_path)))  # размер закаченного файла                                    

                                    if os.path.isfile(scene_path):
                                        if real_file_len != dwnld_file_len:                                            
                                            os.remove(scene_path)
                                            print u'<= DEL, файл не докачался'

                                    # print real_file_len
                                    # print dwnld_file_len
                                    # print real_file_len == dwnld_file_len
                                    # print '-'*10

                                    # проверка архива
                                    # test_gz_archive(scene_path, GZIP_path = ur'G:\Install\GZIP\gzip.exe')

                                    if scene_num + 1 != len(dwnld_list):  # вывести запятую
                                        print ',',

                                # если ошибка при закачке - удалить недокаченный файл
                                except:
                                    print u'<= DEL,',
                                    if os.path.isfile(scene_path):
                                        os.remove(scene_path)

                                    traceback.print_exc()  # напечатать ошибку

                                time_end = Time_now()  # текущее время (конец закачки)

                                # если закачка была менее или равно 60 минут назад
                                if Time_elapsed(time_start, time_end) <= 60 * 60:
                                    logout(apiKey)
                                    apiKey = login(username, password, catalogId)  # авторизация

                                elif Time_elapsed(time_start, time_end) > 60 * 60:
                                    apiKey = login(username, password, catalogId)  # авторизация

            # если авторизация была успешной - удалить токен авторизации
            if apiKey is not None: logout(apiKey)

        # если в процессе выполнения была ошибка
        except:
            try:
                logout(apiKey)  # удалить токен авторизации
            except:
                pass
            print
            traceback.print_exc()  # напечатать ошибку

        print time.strftime("%d.%m.%Y %H:%M:%S") + u' =========== Повтор через час ===========\n'
        time.sleep(3600)


if __name__ == "__main__":

    WRS_2_Path_Row_list=[
        [165, 14], [166, 14],
    ]

    WRS_1_Path_Row_list=[
        [182, 13], [176, 14],
    ]


    main(
        username='username',
        password='password',
        catalogId = "EE",  # возможные параметры catalogId: "EE" "GLOVIS" "HDDS" "LPCS"

        datasets=[
            'LANDSAT_8_C1',
##            'LANDSAT_8_PREWRS',
##            'LANDSAT_ETM_C1',
##            'LANDSAT_TM_C1',
##            'LANDSAT_MSS',
        ],
        WRS_2_Path_Row_list=WRS_2_Path_Row_list,
        WRS_1_Path_Row_list=WRS_1_Path_Row_list,
        archive_path=ur"S:\Landsat",
        temp_dwnld_folder=ur'G:\temp'
    )

    # LANDSAT_8_C1          Landsat 8 Operational Land Imager and Thermal Infrared Sensor Collection 1 Level-1
    # LANDSAT_8_PREWRS      Landsat 8 Operational Land Imager and Thermal Infrared Sensor Pre-WRS-2: 2013
    # LANDSAT_ETM_C1        Landsat 7 Enhanced Thematic Mapper Plus Collection 1 Level-1
    # LANDSAT_TM_C1         Landsat 4-5 Thematic Mapper Collection 1 Level-1
    # LANDSAT_MSS           Landsat 1-5 Multispectral Scanner: 1972-2013