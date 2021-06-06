from app import app
import json
import unittest

class AppTestCase(unittest.TestCase):
  def setUp(self):
    self.client = app.test_client(self)

  def recognize_data(self):
    return {
      "image": (open('tests/fixtures/image.jpg', 'rb'), 'image.jpg')
    }
  
  def test_get_index(self):
    resp = self.client.get("/")
    self.assertEqual(resp.status_code, 200)
    resp_text = resp.get_data(as_text=True)
    self.assertFalse("Tingkat Kematangan" in resp_text)
    self.assertFalse("Harga Setelah didiskon" in resp_text)
    self.assertFalse("Beli" in resp_text)

  def test_recognition_api_bad_request(self):
    resp = self.client.post("/api/recognize", data={})
    self.assertEqual(resp.status_code, 400)
  
  def test_recognition_api_success(self):
    response = self.client.post("/api/recognize", data=self.recognize_data())
    response_data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(type(response_data["freshness_level"]), int)
    self.assertEqual(type(response_data["price"]), int)

if __name__ == "__main__":
  unittest.main()