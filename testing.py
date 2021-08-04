import requests

sheets = {
    'sheet1': 'https://docs.google.com/spreadsheets/d/14hFn00O9632n96Z2xGWvfrcY-K4kHiOGR02Rx7dsj54/export?format=csv&id=14hFn00O9632n96Z2xGWvfrcY-K4kHiOGR02Rx7dsj54&gid=0',
    'sheet2': 'https://docs.google.com/spreadsheets/d/14hFn00O9632n96Z2xGWvfrcY-K4kHiOGR02Rx7dsj54/export?format=csv&id=14hFn00O9632n96Z2xGWvfrcY-K4kHiOGR02Rx7dsj54&gid=447738801'
}

for sheet in list(sheets.keys()):
    response = requests.get(sheets[sheet])
    with open(f'{sheet}.csv', 'wb') as csvfile:
        csvfile.write(response.content)