from django.test import TestCase
from django.urls.base import reverse

from .models import NewsStory
from dateutil import parser


class NewsStoryTests(TestCase):
    def setUp(self):
        self.news_story = NewsStory.objects.create(
            headline="Russia claims full control of Mariupol, says steel mill is completely liberated",
            description="A convoy of Russian armoured vehicles drives along a road in the course of Ukraine-Russia "
                        "conflict near Mariupol in the Donetsk region, Ukraine May 20, 2022. ",
            date_time=parser.parse("May 20, 2022 12:00 +0000"),
            link="https://www.cbc.ca/news/world/russia-ukraine-war-1.6460410?cmp=rss",
            image="https://i.cbc.ca/1.6461351.1653074708!/fileImage/httpImage/image.JPG_gen/derivatives/16x9_460"
                  "/ukraine-crisis-mariupol.JPG",
            sources=["CBC"],
            relevancy=100
        )

    def test_episode_content(self):
        self.assertEqual(self.news_story.description, "A convoy of Russian armoured vehicles drives along a road in "
                                                      "the course of Ukraine-Russia conflict near Mariupol in the "
                                                      "Donetsk region, Ukraine May 20, 2022. ")
        self.assertEqual(self.news_story.link, "https://www.cbc.ca/news/world/russia-ukraine-war-1.6460410?cmp=rss")
        self.assertEqual(self.news_story.relevancy, 100)
        self.assertEqual(str(self.news_story.date_time), "2022-05-20 12:00:00+00:00")

    def test_episode_str_representation(self):
        self.assertEqual(
            str(self.news_story), "CBC: Russia claims full control of Mariupol, says steel mill is completely "
                                  "liberated"
        )

    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")

    def test_homepage_list_contents(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Russia claims full control of Mariupol, says steel mill is completely liberated")
