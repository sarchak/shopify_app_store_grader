import requests
import regex as re
from bs4 import BeautifulSoup
from utils import exception
import string

class App:
  def __init__(self, url):
    """
      Class definition for scrapying an app url
    """
    page = requests.get(url)
    self.url = url
    self.soup = BeautifulSoup(page.text, 'html.parser')


  @exception
  def heading(self):
    """ Extract Heading Information"""
    return self.soup.find_all(class_='heading--2 ui-app-store-hero__header__app-name')[0].text

  @exception
  def tagline(self):
    return self.soup.find_all(class_='heading--3 ui-app-store-hero__description')[0].text

  @exception
  def rating(self):
    return self.soup.find_all(class_='ui-star-rating__rating')[0].text


  @exception
  def reviews(self):
    return self.soup.find_all(class_='ui-review-count-summary')[0].text


  @exception
  def video(self):
    return self.soup.find_all(class_='ui-app-store-hero__media__video')[0]['src']


  @exception
  def key_benefits(self):
    return self.soup.find_all(class_='key-benefits-section')[0].text


  @exception
  def description(self):
    text = self.soup.find_all(class_='grid__item grid__item--tablet-up-two-thirds grid__item--desktop-up-6 app-listing-description')[0].text
    text = text.replace('\n', ' ')
    words = text.split()
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in words]
    return ' '.join(stripped)

  @exception
  def description_raw(self):
    return self.soup.find_all(class_='grid__item grid__item--tablet-up-two-thirds grid__item--desktop-up-6 app-listing-description')[0]


  @exception
  def pricing(self):
    return self.soup.find_all(class_='section background-light color-ink app-listing__pricing app-listing__pricing--multiple')[0].text


  @exception
  def categories(self):
    return self.soup.find_all(class_='heading--5 ui-app-store-hero__kicker')[0].text


  @exception
  def has_list_elements(self):
    tmp = self.description_raw()
    return len(tmp.find_all('li'))

  @exception
  def boolean_fields(self):
    faq = False
    developer_website = False
    priv_policy = False
    phone_number = False
    email = False

    regex = r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
    reg_email = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    for t in self.soup.find_all(class_='app-support-list__item'):
      clean_text = None
      try:
        clean_text = t.find_all('a')[0].text.strip()
      except:
        clean_text = t.text.strip()

      if clean_text == 'FAQ':
        faq=True
      if clean_text == 'Developer website':
        developer_website = True
      if clean_text == 'Privacy policy':
        priv_policy = True
      if re.search(regex, clean_text):
        phone_number = True
      if re.search(reg_email, clean_text):
        email = True

    return {
      'faq':faq,
      'developer_website': developer_website,
      'privacy_policy': priv_policy,
      'phone_number': phone_number,
      'email': email
    }

  def data(self):
    fields = {
      'url': self.url,
      'heading': self.heading(),
      'tagline': self.tagline(),
      'rating': self.rating(),
      'reviews': self.reviews(),
      'video': self.video(),
      'description': self.description(),
      'list_elements': self.has_list_elements(),
      'pricing': self.pricing(),
      'categories': self.categories(),
    }
    return {**fields, **self.boolean_fields()}
