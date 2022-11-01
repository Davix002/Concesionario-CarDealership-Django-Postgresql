from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.files import File
from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

from .models import Car, Order, User



# Create your tests here.
class RegistrationTestCase(LiveServerTestCase):

    def setUp(self):
        options = Options()
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        self.selenium = webdriver.Firefox(options=options)
        super(RegistrationTestCase, self).setUp()
        self.url = self.live_server_url + reverse('web:register')

    def tearDown(self):
        self.selenium.quit()
        super(RegistrationTestCase, self).tearDown()

    # With correct details
    def test_register(self):
        selenium = self.selenium
        selenium.get(self.url)
        print("\nTesteando el sistema de registro")

        # Now open the link for registration
        first_name = selenium.find_element_by_id('id_first_name')
        last_name = selenium.find_element_by_id('id_last_name')
        email = selenium.find_element_by_id('id_email')
        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        identificacion = selenium.find_element_by_id('id_identificacion')
        telefono = selenium.find_element_by_id('id_telefono')
        pais = selenium.find_element_by_id('id_pais')
        departamento = selenium.find_element_by_id('id_departamento')
        ciudad = selenium.find_element_by_id('id_ciudad')
        direccion = selenium.find_element_by_id('id_direccion')
        submit = selenium.find_element_by_id('register')

        first_name.send_keys('Test')
        last_name.send_keys('User')
        email.send_keys('test@user.com')
        username.send_keys('testuser')
        password.send_keys('testuser')
        identificacion.send_keys('test_identificacion')
        telefono.send_keys('test_telefono')
        pais.send_keys('test_pais')
        departamento.send_keys('test_departamento')
        ciudad.send_keys('test_ciudad')
        direccion.send_keys('test_direccion')

        # submitting the form
        submit.click()

        assert "Panel de control" in selenium.title

    # With existing username
    def test_register_blankuser(self):
        selenium = self.selenium

        # Do the registration
        user = User.objects.create_user(username="testuser", email="test@user.com", password="testuser")

        # Logout and repeat the test
        selenium.get(self.live_server_url + reverse('web:logout'))
        selenium.get(self.url)
        print("\nTesteando el registro de un usuario repetido")

        first_name = selenium.find_element_by_id('id_first_name')
        last_name = selenium.find_element_by_id('id_last_name')
        email = selenium.find_element_by_id('id_email')
        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        identificacion = selenium.find_element_by_id('id_identificacion')
        telefono = selenium.find_element_by_id('id_telefono')
        pais = selenium.find_element_by_id('id_pais')
        departamento = selenium.find_element_by_id('id_departamento')
        ciudad = selenium.find_element_by_id('id_ciudad')
        direccion = selenium.find_element_by_id('id_direccion')
        submit = selenium.find_element_by_id('register')

        first_name.send_keys('Test')
        last_name.send_keys('User')
        email.send_keys('test@user.com')
        username.send_keys('testuser')
        password.send_keys('testuser')
        identificacion.send_keys('test_identificacion')
        telefono.send_keys('test_telefono')
        pais.send_keys('test_pais')
        departamento.send_keys('test_departamento')
        ciudad.send_keys('test_ciudad')
        direccion.send_keys('test_direccion')

        # submitting the form
        submit.click()

        self.assertInHTML("Ya existe un usuario con este nombre.", selenium.page_source)


class LoginTestCase(LiveServerTestCase):

    def setUp(self):
        options = Options()
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        self.selenium = webdriver.Firefox(options=options)
        super(LoginTestCase, self).setUp()
        self.url = self.live_server_url + reverse('web:login')
        self.user = User.objects.create_user(username="testuser", email="test@user.com", password="testuser")

    def tearDown(self):
        self.selenium.quit()
        super(LoginTestCase, self).tearDown()

    def test_login(self): 
        print("\nCorriendo Test de login")
        selenium = self.selenium

        selenium.get(self.url)
        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('submit')

        username.send_keys('testuser')
        password.send_keys('testuser')
        submit.click()

        assert "Vehiculos" in selenium.title
        self.assertInHTML(self.user.last_name, selenium.page_source)

    def test_invalid_login(self):
        print("\nTesteando login inválidos")
        selenium = self.selenium

        selenium.get(self.url)
        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('submit')

        # Wrong username

        username.send_keys('wrong')
        password.send_keys('testuser')
        submit.click()

        self.assertEqual("login inválido", selenium.find_element_by_id("error").text)

        # Wrong password

        selenium.get(self.url)
        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('submit')

        username.send_keys('testuser')
        password.send_keys('wrong')
        submit.click()

        self.assertEqual("login inválido", selenium.find_element_by_id("error").text)

        # Blank details

        selenium.get(self.url)
        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_id('submit')

        username.send_keys('')
        password.send_keys('')
        submit.click()

        self.assertEqual("login inválido", selenium.find_element_by_id("error").text)


class AdminCarTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', email='admin@admin.com', password='djangoadmin')
        self.user.is_active = True
        self.user.save()

    def tearDown(self):
        super(AdminCarTest, self).tearDown()

    def test_car_add(self):
        print("\nTesteando añadir vehículo...")
        user = self.user
        car = Car(
            foto=File(open(settings.BASE_DIR + settings.STATIC_URL + 'images/car.jpg', 'r')),
            marca='Marca',
            modelo='Modelo',
            anio='2022',
            combustible='Gasolina',
            puertas=4,
            transmision='Automatica',
            motor=1.4,
            potencia='140 HP',
            tipo='Ligero',
            consumo=4.8,
            estado='Nuevo',
            kilometros=0,
            pais='Colombia',
            descripcion='Carro de testeo de pagina',
            precio=65000000,
            anadido_por=user,
            
        )

        self.assertEqual(car.__str__(), "Marca Modelo")


class OrderTest(StaticLiveServerTestCase):
    def setUp(self):
        options = Options()
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        self.selenium = webdriver.Firefox(options=options)
        self.su = User.objects.create_superuser(username='admin', email='admin@admin.com', password='djangoadmin')
        self.su.is_active = True
        self.su.save()
        self.user = User.objects.create_superuser(username='testuser', email='test@user.com', password='testuser')
        self.user.first_name = "Test"
        self.user.last_name = "User"
        self.user.is_active = True
        self.user.save()
        super(OrderTest, self).setUp()
        # Create a car so that a view will be available
        car = Car.objects.create(
            foto=File(open(settings.BASE_DIR + '/media/car.jpg', 'rb')),
            marca='Marca',
            modelo='Modelo',
            anio='2022',
            combustible='Gasolina',
            puertas=4,
            transmision='Automatica',
            motor=1.4,
            potencia='140 HP',
            tipo='Ligero',
            consumo=4.8,
            estado='Nuevo',
            kilometros=0,
            pais='Colombia',
            descripcion='Carro de testeo de pagina',
            precio=65000000,
            anadido_por=self.su
        )

        self.pk = car.id
        self.url = self.live_server_url + reverse("web:details", args=[self.pk])
        # Login with the account
        self.selenium.get(self.live_server_url + reverse("web:login"))
        username = self.selenium.find_element_by_id('id_username')
        password = self.selenium.find_element_by_id('id_password')
        submit = self.selenium.find_element_by_id('submit')

        username.send_keys('testuser')
        password.send_keys('testuser')
        submit.click()
        time.sleep(4)

    def tearDown(self):
        self.selenium.quit()
        super(OrderTest, self).tearDown()

    def test_order(self):
        print("\nTesteando comprar vehículo...")
        selenium = self.selenium

        selenium.get(self.url)

        order_btn = selenium.find_element_by_id("orderBtn")
        pais = selenium.find_element_by_id("id_pais")
        departamento = selenium.find_element_by_id("id_departamento")
        ciudad = selenium.find_element_by_id("id_ciudad")
        submit = selenium.find_element_by_id("clickBtn")
        address = selenium.find_element_by_id("address")
        identificacion = selenium.find_element_by_id("id_identificacion")

        order_btn.click()

        time.sleep(1)
        element = selenium.switch_to.active_element
        time.sleep(1)
        pais.send_keys('test_pais')
        departamento.send_keys('test_departamento')
        ciudad.send_keys('test_ciudad')
        address.send_keys('test_address')
        identificacion.send_keys('test_identificacion')
        submit.click()
        time.sleep(1)
        td = Order.objects.get(user=self.user)
        self.assertEqual(td.__str__(), "Test User - Modelo")