from app import App
import pandas as pd
from multiprocessing import Pool, TimeoutError
import time
import os

app_urls = []
with open('shopify_apps.txt', 'r') as fd:
  for line in fd.readlines():
    app_url = line.strip()
    app_urls.append(app_url)

def get_data(url):
  print("Url : {}".format(url))
  app = App(url)
  return app.data()


pool = Pool(processes=8)
dataset = []
multiple_results = [pool.apply_async(get_data, (i, )) for i in app_urls]

for res in multiple_results:
  dataset.append(res.get())

df = pd.DataFrame(dataset)
df.to_csv('shopify_dataset.csv', sep='|', index=False)
