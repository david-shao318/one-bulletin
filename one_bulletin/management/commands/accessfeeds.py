import logging

from django.conf import settings
from django.core.management.base import BaseCommand

import feedparser
from dateutil import parser
from bs4 import BeautifulSoup

# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger
# from django_apscheduler.jobstores import DjangoJobStore
# from django_apscheduler.models import DjangoJobExecution

from one_bulletin.models import NewsStory

whois_timezone_info = {"A": 1 * 3600, "ACDT": 10.5 * 3600, "ACST": 9.5 * 3600, "ACT": -5 * 3600,
                       "ACWST": 8.75 * 3600, "ADT": 4 * 3600, "AEDT": 11 * 3600, "AEST": 10 * 3600,
                       "AET": 10 * 3600, "AFT": 4.5 * 3600, "AKDT": -8 * 3600, "AKST": -9 * 3600, "ALMT": 6 * 3600,
                       "AMST": -3 * 3600, "AMT": -4 * 3600, "ANAST": 12 * 3600, "ANAT": 12 * 3600, "AQTT": 5 * 3600,
                       "ART": -3 * 3600, "AST": 3 * 3600, "AT": -4 * 3600, "AWDT": 9 * 3600, "AWST": 8 * 3600,
                       "AZOST": 0 * 3600, "AZOT": -1 * 3600, "AZST": 5 * 3600, "AZT": 4 * 3600, "AoE": -12 * 3600,
                       "B": 2 * 3600, "BNT": 8 * 3600, "BOT": -4 * 3600, "BRST": -2 * 3600, "BRT": -3 * 3600,
                       "BST": 6 * 3600, "BTT": 6 * 3600, "C": 3 * 3600, "CAST": 8 * 3600, "CAT": 2 * 3600,
                       "CCT": 6.5 * 3600, "CDT": -5 * 3600, "CEST": 2 * 3600, "CET": 1 * 3600,
                       "CHADT": 13.75 * 3600, "CHAST": 12.75 * 3600, "CHOST": 9 * 3600, "CHOT": 8 * 3600,
                       "CHUT": 10 * 3600, "CIDST": -4 * 3600, "CIST": -5 * 3600, "CKT": -10 * 3600,
                       "CLST": -3 * 3600, "CLT": -4 * 3600, "COT": -5 * 3600, "CST": -6 * 3600, "CT": -6 * 3600,
                       "CVT": -1 * 3600, "CXT": 7 * 3600, "ChST": 10 * 3600, "D": 4 * 3600, "DAVT": 7 * 3600,
                       "DDUT": 10 * 3600, "E": 5 * 3600, "EASST": -5 * 3600, "EAST": -6 * 3600, "EAT": 3 * 3600,
                       "ECT": -5 * 3600, "EDT": -4 * 3600, "EEST": 3 * 3600, "EET": 2 * 3600, "EGST": 0 * 3600,
                       "EGT": -1 * 3600, "EST": -5 * 3600, "ET": -5 * 3600, "F": 6 * 3600, "FET": 3 * 3600,
                       "FJST": 13 * 3600, "FJT": 12 * 3600, "FKST": -3 * 3600, "FKT": -4 * 3600, "FNT": -2 * 3600,
                       "G": 7 * 3600, "GALT": -6 * 3600, "GAMT": -9 * 3600, "GET": 4 * 3600, "GFT": -3 * 3600,
                       "GILT": 12 * 3600, "GMT": 0 * 3600, "GST": 4 * 3600, "GYT": -4 * 3600, "H": 8 * 3600,
                       "HDT": -9 * 3600, "HKT": 8 * 3600, "HOVST": 8 * 3600, "HOVT": 7 * 3600, "HST": -10 * 3600,
                       "I": 9 * 3600, "ICT": 7 * 3600, "IDT": 3 * 3600, "IOT": 6 * 3600, "IRDT": 4.5 * 3600,
                       "IRKST": 9 * 3600, "IRKT": 8 * 3600, "IRST": 3.5 * 3600, "IST": 5.5 * 3600, "JST": 9 * 3600,
                       "K": 10 * 3600, "KGT": 6 * 3600, "KOST": 11 * 3600, "KRAST": 8 * 3600, "KRAT": 7 * 3600,
                       "KST": 9 * 3600, "KUYT": 4 * 3600, "L": 11 * 3600, "LHDT": 11 * 3600, "LHST": 10.5 * 3600,
                       "LINT": 14 * 3600, "M": 12 * 3600, "MAGST": 12 * 3600, "MAGT": 11 * 3600, "MART": 9.5 * 3600,
                       "MAWT": 5 * 3600, "MDT": -6 * 3600, "MHT": 12 * 3600, "MMT": 6.5 * 3600, "MSD": 4 * 3600,
                       "MSK": 3 * 3600, "MST": -7 * 3600, "MT": -7 * 3600, "MUT": 4 * 3600, "MVT": 5 * 3600,
                       "MYT": 8 * 3600, "N": -1 * 3600, "NCT": 11 * 3600, "NDT": 2.5 * 3600, "NFT": 11 * 3600,
                       "NOVST": 7 * 3600, "NOVT": 7 * 3600, "NPT": 5.5 * 3600, "NRT": 12 * 3600, "NST": 3.5 * 3600,
                       "NUT": -11 * 3600, "NZDT": 13 * 3600, "NZST": 12 * 3600, "O": -2 * 3600, "OMSST": 7 * 3600,
                       "OMST": 6 * 3600, "ORAT": 5 * 3600, "P": -3 * 3600, "PDT": -7 * 3600, "PET": -5 * 3600,
                       "PETST": 12 * 3600, "PETT": 12 * 3600, "PGT": 10 * 3600, "PHOT": 13 * 3600, "PHT": 8 * 3600,
                       "PKT": 5 * 3600, "PMDT": -2 * 3600, "PMST": -3 * 3600, "PONT": 11 * 3600, "PST": -8 * 3600,
                       "PT": -8 * 3600, "PWT": 9 * 3600, "PYST": -3 * 3600, "PYT": -4 * 3600, "Q": -4 * 3600,
                       "QYZT": 6 * 3600, "R": -5 * 3600, "RET": 4 * 3600, "ROTT": -3 * 3600, "S": -6 * 3600,
                       "SAKT": 11 * 3600, "SAMT": 4 * 3600, "SAST": 2 * 3600, "SBT": 11 * 3600, "SCT": 4 * 3600,
                       "SGT": 8 * 3600, "SRET": 11 * 3600, "SRT": -3 * 3600, "SST": -11 * 3600, "SYOT": 3 * 3600,
                       "T": -7 * 3600, "TAHT": -10 * 3600, "TFT": 5 * 3600, "TJT": 5 * 3600, "TKT": 13 * 3600,
                       "TLT": 9 * 3600, "TMT": 5 * 3600, "TOST": 14 * 3600, "TOT": 13 * 3600, "TRT": 3 * 3600,
                       "TVT": 12 * 3600, "U": -8 * 3600, "ULAST": 9 * 3600, "ULAT": 8 * 3600, "UTC": 0 * 3600,
                       "UYST": -2 * 3600, "UYT": -3 * 3600, "UZT": 5 * 3600, "V": -9 * 3600, "VET": -4 * 3600,
                       "VLAST": 11 * 3600, "VLAT": 10 * 3600, "VOST": 6 * 3600, "VUT": 11 * 3600, "W": -10 * 3600,
                       "WAKT": 12 * 3600, "WARST": -3 * 3600, "WAST": 2 * 3600, "WAT": 1 * 3600, "WEST": 1 * 3600,
                       "WET": 0 * 3600, "WFT": 12 * 3600, "WGST": -2 * 3600, "WGT": -3 * 3600, "WIB": 7 * 3600,
                       "WIT": 9 * 3600, "WITA": 8 * 3600, "WST": 14 * 3600, "WT": 0 * 3600, "X": -11 * 3600,
                       "Y": -12 * 3600, "YAKST": 10 * 3600, "YAKT": 9 * 3600, "YAPT": 10 * 3600, "YEKST": 6 * 3600,
                       "YEKT": 5 * 3600, "Z": 0 * 3600}

feed_urls = {
    "CBC World": "https://rss.cbc.ca/lineup/world.xml",
    "CBC Canada": "https://rss.cbc.ca/lineup/canada.xml",
    "CBC Politics": "https://rss.cbc.ca/lineup/politics.xml",
    "CBC Business": "https://rss.cbc.ca/lineup/business.xml",
    "CBC Health": "https://rss.cbc.ca/lineup/health.xml",
    "CBC Arts & Entertainment": "https://rss.cbc.ca/lineup/arts.xml",
    "CBC Technology & Science": "https://rss.cbc.ca/lineup/technology.xml",
    "CBC British Columbia": "https://rss.cbc.ca/lineup/canada-britishcolumbia.xml",
    "CBC Calgary": "https://rss.cbc.ca/lineup/canada-calgary.xml",
    "CBC Toronto": "https://rss.cbc.ca/lineup/canada-toronto.xml",
    "CBC Montreal": "https://rss.cbc.ca/lineup/canada-montreal.xml",
    "CBC Top Stories": "https://rss.cbc.ca/lineup/topstories.xml",
    "NYT Home Page": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "NYT World": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "NYT US": "https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
    "NYT Business": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
    "NYT Technology": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "ECONOMIST Leaders": "https://www.economist.com/leaders/rss.xml",
    "ECONOMIST Briefing": "https://www.economist.com/briefing/rss.xml",
}

logger = logging.getLogger(__name__)


# access CBC feeds
def access_cbc(url):
    # parse feed
    feed = feedparser.parse(url)
    feed_src = feed.feed.title
    feed_len = len(feed.entries)

    # iterate through all stories
    for i in range(feed_len):
        item = feed.entries[i]

        # add to relevancy score if story already exists (but is not in the same feed)
        if NewsStory.objects.filter(link=item.links[0].href).exists():
            story = NewsStory.objects.get(link=item.links[0].href)
            if feed_src not in story.sources:
                story.sources.append(feed_src)
                story.relevancy += 100 - (i * 100 // feed_len)
            story.save()

        # otherwise add story to db
        else:
            soup = BeautifulSoup(item.summary, features="html.parser")
            descr = list(soup.findAll("p"))
            if str(descr[0]) == "<p></p>":
                descr = item.title
            else:
                descr = descr[0].string
            story = NewsStory(
                headline=item.title,
                description=descr,
                date_time=parser.parse(item.published, tzinfos=whois_timezone_info),
                link=item.links[0].href,
                image=soup.img['src'],
                sources=[feed_src],
                relevancy=100 - (i * 100 // feed_len)
            )
            story.save()


# access NYT feeds
def access_nyt(url):
    # parse feed
    feed = feedparser.parse(url)
    feed_src = feed.feed.title
    feed_len = len(feed.entries)

    for i in range(feed_len):
        item = feed.entries[i]

        # add to relevancy score if story already exists (but is not in the same feed)
        if NewsStory.objects.filter(link=item.links[0].href).exists():
            story = NewsStory.objects.get(link=item.links[0].href)
            if feed_src not in story.sources:
                story.sources.append(feed_src)
                story.relevancy += 120 - (i * 120 // feed_len)
            story.save()

        # otherwise add story to db
        else:
            if 'media_content' not in item:
                img_url = "static/imgs/nyt.svg"
            else:
                img_url = item.media_content[0]['url']
            story = NewsStory(
                headline=item.title,
                description=item.summary,
                date_time=parser.parse(item.published, tzinfos=whois_timezone_info),
                link=item.links[0].href,
                image=img_url,
                sources=[feed_src],
                relevancy=120 - (i * 120 // feed_len)
            )
            story.save()


# access The Economist feeds
def access_economist(url, num_art):
    # parse feed
    feed = feedparser.parse(url)
    feed_src = "The Economist: " + feed.feed.title

    for i in range(num_art):
        item = feed.entries[i]

        # add to relevancy score if story already exists (but is not in the same feed)
        if NewsStory.objects.filter(link=item.links[0].href).exists():
            story = NewsStory.objects.get(link=item.links[0].href)
            if feed_src not in story.sources:
                story.sources.append(feed_src)
                story.relevancy += 250 - (i * 250 // num_art)
            story.save()

        # otherwise add story to db
        else:
            story = NewsStory(
                headline=item.title,
                description=item.summary,
                date_time=parser.parse(item.published, tzinfos=whois_timezone_info),
                link=item.links[0].href,
                image="static/imgs/economist.svg",
                sources=[feed_src],
                relevancy=250 - (i * 250 // num_art)
            )
            story.save()


def get_all_new_feeds():
    # reset relevancy scores
    story_set = NewsStory.objects.all()
    for st in story_set.iterator():
        st.sources = list()
        st.relevancy = 0
        st.save()

    # go through all feeds and access stories
    for name, url in feed_urls.items():
        if name[0] == 'C':
            access_cbc(url)
        elif name[0] == 'N':
            access_nyt(url)
        elif name == "ECONOMIST Leaders":
            access_economist(url, 20)
        elif name == "ECONOMIST Briefing":
            access_economist(url, 3)

    # remove stories with zero relevancy
    NewsStory.objects.filter(relevancy=0).delete()


class Command(BaseCommand):
    help = "Runs apscheduler to access all feeds on set intervals."

    def handle(self, *args, **options):
        get_all_new_feeds()

        # scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        # scheduler.add_jobstore(DjangoJobStore(), "default")
        #
        # scheduler.add_job(
        #     get_all_new_feeds,
        #     trigger="interval",
        #     minutes=30,
        #     id="one bulletin News Feeds",
        #     max_instances=1,
        #     replace_existing=True,
        # )
        # logger.info("Added job: one bulletin FEEDS")
        #
        # try:
        #     logger.info("Starting scheduler...")
        #     scheduler.start()
        # except KeyboardInterrupt:
        #     logger.info("Stopping scheduler...")
        #     scheduler.shutdown()
        #     logger.info("Scheduler shut down successfully!")
        # return
