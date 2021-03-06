import datetime

from mediacloud.test.basetest import AdminApiBaseTest
from mediacloud.test import QUERY_LAST_WEEK

SENTENCE_COUNT = 100
QUERY_TEST = "*"


class AdminApiSentencesTest(AdminApiBaseTest):

    def testSentenceListRows(self):
        results = self._mc.sentenceList(QUERY_TEST, QUERY_LAST_WEEK, rows=13)
        self.assertGreater(len(results), 13)
        results = self._mc.sentenceList(QUERY_TEST, QUERY_LAST_WEEK, rows=513)
        self.assertGreater(len(results), 513)

    def testSentenceList(self):
        results = self._mc.sentenceList(QUERY_TEST, QUERY_LAST_WEEK)
        self.assertGreater(len(results), 1000)

    def testSentenceListPaging(self):
        results_page1 = self._mc.sentenceList(QUERY_TEST, QUERY_LAST_WEEK, 0, 10)
        self.assertGreater(len(results_page1), 10)
        page1_sentence_ids = [s['story_sentences_id'] for s in results_page1]
        results_page2 = self._mc.sentenceList(QUERY_TEST, QUERY_LAST_WEEK, 10, 10)
        page2_sentence_ids = [s['story_sentences_id'] for s in results_page2]
        # intersect
        in_both = list(set(page1_sentence_ids) & set(page2_sentence_ids))
        self.assertEqual(len(in_both), 0)

    def testSentenceListSortingAscending(self):
        results = self._mc.sentenceList(QUERY_TEST, QUERY_LAST_WEEK, 0, SENTENCE_COUNT, self._mc.SORT_PUBLISH_DATE_ASC)
        self.assertGreater(len(results), SENTENCE_COUNT)
        last_date = None
        for sentence in results:
            this_date = datetime.datetime.strptime(sentence['publish_date'], self._mc.SENTENCE_PUBLISH_DATE_FORMAT)
            this_date = this_date.replace(second=0, microsecond=0)  # sorting is by minute
            if last_date is not None:
                self.assertLessEqual(last_date, this_date)
                last_date = this_date
            last_date = this_date

    def testSentenceListSortingDescending(self):
        results = self._mc.sentenceList(QUERY_TEST, QUERY_LAST_WEEK, 0, SENTENCE_COUNT, self._mc.SORT_PUBLISH_DATE_DESC)
        self.assertGreater(len(results), SENTENCE_COUNT)
        last_date = None
        for sentence in results:
            this_date = datetime.datetime.strptime(sentence['publish_date'], self._mc.SENTENCE_PUBLISH_DATE_FORMAT)
            this_date = this_date.replace(second=0, microsecond=0)  # sorting is by minute
            if last_date is not None:
                self.assertGreaterEqual(last_date, this_date)
                last_date = this_date
            last_date = this_date

    def testSentenceListSortingRadom(self):
        # we do random sort by telling we want the random sort, and then offsetting to a different start index
        results1 = self._mc.sentenceList(QUERY_TEST, QUERY_LAST_WEEK, 0, SENTENCE_COUNT, self._mc.SORT_RANDOM)
        self.assertGreater(len(results1), SENTENCE_COUNT)
        results2 = self._mc.sentenceList(QUERY_TEST, QUERY_LAST_WEEK, SENTENCE_COUNT * 2, SENTENCE_COUNT, self._mc.SORT_RANDOM)
        self.assertGreater(len(results2), SENTENCE_COUNT)
        for idx in range(0, SENTENCE_COUNT):
            self.assertNotEqual(results1[idx]['stories_id'],
                                results2[idx]['stories_id'],
                                "Stories in two different random sets are the same :-(")
