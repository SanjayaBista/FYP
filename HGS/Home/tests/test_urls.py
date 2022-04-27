from os import remove
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Home.views import home, categoryItem, aboutUs, add_wishlist,remove_wishlist, productDetail, addComment, contactUs
from Account.views import userLogin, userRegister, profile, userLogout, wishlist
class TestUrls(SimpleTestCase):
    def test_list_url_resolves(self):
        url = reverse('home:home')
        self.assertEquals(resolve(url).func, home )

    def test_aboutUs_url_resolves(self):
        url = reverse('home:aboutUs')
        self.assertEquals(resolve(url).func, aboutUs )
    
    def test_add_wishlist_url_resolves(self):
        url = reverse('home:add_wishlist', args=['1'])
        self.assertEquals(resolve(url).func, add_wishlist )

    def test_remove_wishlist_url_resolves(self):
        url = reverse('home:remove_wishlist')
        self.assertEquals(resolve(url).func, remove_wishlist )    

    def test_categoryItem_url_resolves(self):
        url = reverse('home:categoryItem', args=['1','name'])
        self.assertEquals(resolve(url).func, categoryItem )
    
    def test_product_detail_url_resolves(self):
        url = reverse('home:productDetail',args=['1','name'])
        self.assertEquals(resolve(url).func, productDetail )

    def test_add_comment_url_resolves(self):
        url = reverse('home:addComment', args=['1'])
        self.assertEquals(resolve(url).func, addComment )

    def test_contact_us_url_resolves(self):
        url = reverse('home:contactUs')
        self.assertEquals(resolve(url).func, contactUs )

    def test_userLogin_url_resolves(self):
        url = reverse('account:login')
        self.assertEquals(resolve(url).func, userLogin )
    
    def test_userLogout_url_resolves(self):
        url = reverse('account:logout')
        self.assertEquals(resolve(url).func, userLogout )

    def test_userRegister_url_resolves(self):
        url = reverse('account:register')
        self.assertEquals(resolve(url).func, userRegister )
    
  
    def test_profile_url_resolves(self):
        url = reverse('account:profile')
        self.assertEquals(resolve(url).func, profile )

    def test_wishlist_url_resolves(self):
        url = reverse('account:wishlist')
        self.assertEquals(resolve(url).func, wishlist )
    