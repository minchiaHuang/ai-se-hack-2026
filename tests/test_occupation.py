"""Which covered occupation a resume is about, or none: never a guess dressed as one."""
import json
import unittest
from unittest import mock

from skeleton import app
from skeleton.core import occupation
from tests.test_http import Server

COOK = "PROFILE\nHead cook with six years of experience running a restaurant kitchen."
IT = "WORK EXPERIENCE\nIT support at IKEA, helping customers manage subscriptions."


def model_says(text):
    sent = []

    def post(url, headers, payload):
        sent.append(payload)
        return {"content": [{"type": "text", "text": text}]}
    post.sent = sent
    return post


def broken(*args, **kwargs):
    raise OSError("venue wifi")


class Covered(unittest.TestCase):
    def test_the_covered_occupations_are_the_reference_data(self):
        keys = [o["key"] for o in occupation.covered()]
        self.assertEqual(sorted(keys), ["aged_care", "cookery", "welding"])
        self.assertTrue(all(o["label"] for o in occupation.covered()))


class Suggest(unittest.TestCase):
    def test_a_covered_answer_is_returned_with_its_label(self):
        post = model_says('{"occupation": "cookery"}')
        body = occupation.suggest(COOK, post=post, api_key="k")
        self.assertEqual(body, {"occupation": "cookery", "label": "Commercial cook"})
        self.assertEqual(json.loads(post.sent[0]["messages"][0]["content"])["resume"], COOK)

    def test_none_says_it_is_not_covered(self):
        body = occupation.suggest(IT, post=model_says('{"occupation": "none"}'), api_key="k")
        self.assertEqual(body, {"occupation": "none", "label": None})

    def test_an_answer_outside_the_list_is_not_trusted(self):
        for said in ('{"occupation": "it_support"}', "cook", '{"occupation": null}'):
            with self.subTest(said=said):
                body = occupation.suggest(COOK, post=model_says(said), api_key="k")
                self.assertTrue(body["offline"])

    def test_no_key_or_no_network_is_offline_and_nothing_is_guessed(self):
        self.assertTrue(occupation.suggest(COOK, post=broken, api_key="")["offline"])
        body = occupation.suggest(COOK, post=broken, api_key="k")
        self.assertTrue(body["offline"])
        self.assertNotIn("occupation", body)


class Route(Server):
    def test_without_a_key_the_route_is_a_200_offline(self):
        status, text = self.post("/api/occupation", {"text": COOK})
        self.assertEqual(status, 200)
        self.assertTrue(json.loads(text)["offline"])

    def test_the_route_passes_the_text_on(self):
        with mock.patch.object(app.occupation, "suggest",
                               return_value={"occupation": "welding", "label": "Welder"}) as suggest:
            status, text = self.post("/api/occupation", {"text": " " + IT + " "})
        self.assertEqual((status, json.loads(text)["occupation"]), (200, "welding"))
        suggest.assert_called_once_with(IT)

    def test_empty_text_is_a_400(self):
        for body in ({}, {"text": ""}, {"text": 5}):
            with self.subTest(body=body):
                self.assertEqual(self.post("/api/occupation", body)[0], 400)


if __name__ == "__main__":
    unittest.main()


class ReviewMenu(unittest.TestCase):
    def test_the_menu_offers_exactly_the_covered_occupations_and_none(self):
        import re
        page = app.REVIEW_PAGE.read_text(encoding="utf-8")
        menu = re.search(r'<select id="occupation">(.*?)</select>', page, re.S).group(1)
        options = dict(re.findall(r'<option value="([a-z_]*)">([^<]+)</option>', menu))
        options.pop("")
        self.assertEqual(options.pop("none"), "Something else (not covered yet)")
        self.assertEqual(options, {o["key"]: o["label"] for o in occupation.covered()})

    def test_the_page_no_longer_assumes_a_cook(self):
        self.assertNotIn('"cookery";', app.REVIEW_PAGE.read_text(encoding="utf-8").split("mockApi")[0])
