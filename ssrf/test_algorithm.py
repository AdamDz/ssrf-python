import logging
from unittest import TestCase
import mox
from datetime import date, timedelta
from ssrf.algorithm import *
from nose.tools import *
logging.basicConfig(format=logging.BASIC_FORMAT, level=logging.DEBUG)

class TestSSRFAlgorithm (TestCase):
    def setUp(self):
        self._global_data = mox.MockObject(SSRFAlgorithmGlobalData)
        self._algorithm = SSRFAlgorithm(self._global_data)

    def test_initial_alg_data(self):
        alg_data = self._algorithm._fill_initial_algorithm_data()
        assert_equals(1, alg_data['num_reviews'])
        assert_equals(2.5, alg_data['avg_grade'])
        assert_equals(0.0, alg_data['difficulty'])
    
    def test__calculate_interval_first_rep(self):
        interval = self._algorithm._calculate_interval(1, 0.0, 0, PRIORITY_MEDIUM)
        self._assert_interval(1, interval)
        interval = self._algorithm._calculate_interval(1, 0.0, 2, PRIORITY_MEDIUM)
        self._assert_interval(1, interval)
        interval = self._algorithm._calculate_interval(1, 0.0, 3, PRIORITY_MEDIUM)
        self._assert_interval(2, interval)
        interval = self._algorithm._calculate_interval(1, 0.0, 5, PRIORITY_MEDIUM)
        self._assert_interval(8, interval)
    
    def test__calculate_interval_consecutive_rep(self):
        interval = self._algorithm._calculate_interval(5, 2.3, 0, PRIORITY_HIGH)
        self._assert_interval(1, interval)
        interval = self._algorithm._calculate_interval(5, 2.3, 2, PRIORITY_HIGH)
        self._assert_interval(2, interval)
        interval = self._algorithm._calculate_interval(5, 2.3, 3, PRIORITY_HIGH)
        self._assert_interval(3, interval)
        interval = self._algorithm._calculate_interval(5, 2.3, 5, PRIORITY_HIGH)
        self._assert_interval(18, interval)
    
    def test__calculate_interval_wrong_num_reviews(self):
        assert_raises(AssertionError, self._algorithm._calculate_interval, 0, 0.0, 0, PRIORITY_MEDIUM)
    
    def test__calculate_interval_wrong_prev_avg_grade(self):
        assert_raises(AssertionError, self._algorithm._calculate_interval, 1, -0.01, 0, PRIORITY_MEDIUM)
        self._algorithm._calculate_interval(1, 0.0, 0, PRIORITY_MEDIUM)
        
        self._algorithm._calculate_interval(1, 5.0, 0, PRIORITY_MEDIUM)
        assert_raises(AssertionError, self._algorithm._calculate_interval, 1, 5.01, 0, PRIORITY_MEDIUM)
        
    def test__calculate_interval_wrong_grade(self):
        assert_raises(AssertionError, self._algorithm._calculate_interval, 1, 0.0, -2, PRIORITY_MEDIUM)
        self._algorithm._calculate_interval(1, 0.0, -1, PRIORITY_MEDIUM)
    
        self._algorithm._calculate_interval(1, 0.0, 5, PRIORITY_MEDIUM)
        assert_raises(AssertionError, self._algorithm._calculate_interval, 1, 0.0, 6, PRIORITY_MEDIUM)
    
    def test__calculate_interval_wrong_priority(self):
        assert_raises(AssertionError, self._algorithm._calculate_interval, 1, 0.0, 0, -3)
        self._algorithm._calculate_interval(1, 0.0, 5, PRIORITY_LOW)
        
        self._algorithm._calculate_interval(1, 0.0, 5, PRIORITY_HIGH)
        assert_raises(AssertionError, self._algorithm._calculate_interval, 1, 0.0, 0, 3)

    def test__find_last_zero_workload_ind_wrong_workloads(self):
        assert_raises(AssertionError, self._algorithm._find_last_zero_workload_ind, [0, -1])
    
    def test__find_max_load_reduction_ind_wrong_intervals(self):
        assert_raises(AssertionError, self._algorithm._find_max_load_reduction_ind, 
                          self._algorithm._fill_initial_algorithm_data(), [0, 1], [0, 0], [0.0, 0.0], PRIORITY_MEDIUM)
        
    def test__find_max_load_reduction_ind_wrong_workloads(self):
        assert_raises(AssertionError, self._algorithm._find_max_load_reduction_ind, 
                          self._algorithm._fill_initial_algorithm_data(), [1, 2], [-1, 0], [0.0, 0.0], PRIORITY_MEDIUM)
        
    def test__find_max_load_reduction_ind_wrong_avg_difficulties(self):
        assert_raises(AssertionError, self._algorithm._find_max_load_reduction_ind, 
                          self._algorithm._fill_initial_algorithm_data(), [1, 2], [0, 0], [-0.01, 0.0], PRIORITY_MEDIUM)
        
    def test__calculate_load_coeffs(self):
        load_coeffs = self._algorithm._calculate_load_coeffs([63, 40, 33, 20, 18, 50], [6.0, 2.2, 1.5, 1.6, 3.5, 5.1])
        self._assert_load_coeffs([0.536, 0.202, 0.103, 0.007, 0.163, 0.454], load_coeffs)
    
    def test__calculate_load_coeffs_0_workload(self):
        # zero workload on some day
        load_coeffs = self._algorithm._calculate_load_coeffs([0, 1], [0.0, 2.08])
        self._assert_load_coeffs([0.0, 1.0], load_coeffs)

    def test__calculate_load_coeffs_min_workload_avg_difficulty_on_same_interval(self):
        # min. workload and min. avg difficulty on the same date
        load_coeffs = self._algorithm._calculate_load_coeffs([5, 3, 2], [0.3, 2.5, 0.1])
        self._assert_load_coeffs([0.402, 0.516, 0.0], load_coeffs)

    def test__calculate_load_coeffs_wrong_workloads(self):
        assert_raises(AssertionError, self._algorithm._calculate_load_coeffs, [0, -1], [0.0, 0.0])
        self._algorithm._calculate_load_coeffs([0, 0], [0.0, 0.0])
        
    def test__calculate_load_coeffs_wrong_avg_difficulties(self):
        assert_raises(AssertionError, self._algorithm._calculate_load_coeffs, [0, 0], [0.0, -0.01])
        self._algorithm._calculate_load_coeffs([0, 0], [0.0, 0.0])
        
    def test__calculate_load_coeffs_workload_avg_difficulties_len_mismatch(self):
        assert_raises(AssertionError, self._algorithm._calculate_load_coeffs, [0, 0], [0.0])
        assert_raises(AssertionError, self._algorithm._calculate_load_coeffs, [0], [0.0, 0.0])
        self._algorithm._calculate_load_coeffs([0, 0], [0.0, 0.0])
        
    def test__calculate_difficulty(self):
        difficulty = self._algorithm._calculate_difficulty(1, PRIORITY_MEDIUM, 1)
        self._assert_difficulty(1.50, difficulty)
        difficulty = self._algorithm._calculate_difficulty(1, PRIORITY_MEDIUM, 2)
        self._assert_difficulty(1.10, difficulty)
        difficulty = self._algorithm._calculate_difficulty(1, PRIORITY_MEDIUM, 7)
        self._assert_difficulty(0.12, difficulty)
        difficulty = self._algorithm._calculate_difficulty(1, PRIORITY_MEDIUM, 8)
        self._assert_difficulty(0.0, difficulty)

    def test_schedule_first_rep_0_grade(self):
        date_from = date.today() + timedelta(1)
        date_to = date.today() + timedelta(1)
        self._global_data.get_workloads(date_from, date_to, None).AndReturn([0])
        mox.Replay(self._global_data)

        next_review, alg_data = self._algorithm.schedule(grade=0)

        mox.Verify(self._global_data)
        assert_equals(date.today() + timedelta(1), next_review.date())
        self._assert_new_alg_data(2, 1.25, 1.50, FINAL_DRILL, alg_data)
        
    def test_schedule_first_rep_2_grade(self):
        date_from = date.today() + timedelta(1)
        date_to = date.today() + timedelta(1)
        self._global_data.get_workloads(date_from, date_to, None).AndReturn([5])
        self._global_data.get_avg_difficulties(date_from, date_to, None).AndReturn([0.88])
        mox.Replay(self._global_data)

        next_review, alg_data = self._algorithm.schedule(grade=2)

        mox.Verify(self._global_data)
        assert_equals(date.today() + timedelta(1), next_review.date())
        self._assert_new_alg_data(2, 2.25, 1.50, FINAL_DRILL, alg_data)
        
    def test_schedule_first_rep_3_grade(self):
        date_from = date.today() + timedelta(1)
        date_to = date.today() + timedelta(2)
        self._global_data.get_workloads(date_from, date_to, None).AndReturn([0, 1])
        mox.Replay(self._global_data)

        next_review, alg_data = self._algorithm.schedule(grade=3)

        mox.Verify(self._global_data)
        assert_equals(date.today() + timedelta(1), next_review.date())
        self._assert_new_alg_data(2, 2.75, 1.50, MEMORIZED, alg_data)

    def test_schedule_first_rep_5_grade(self):
        date_from = date.today() + timedelta(4)
        date_to = date.today() + timedelta(8)
        self._global_data.get_workloads(date_from, date_to, None).AndReturn([5, 3, 2, 4, 8])
        self._global_data.get_avg_difficulties(date_from, date_to, None).AndReturn([2.5, 0.3, 0.1, 1.1, 0.8])
        mox.Replay(self._global_data)

        next_review, alg_data = self._algorithm.schedule(grade=5)
        
        mox.Verify(self._global_data)
        assert_equals(date.today() + timedelta(5), next_review.date())
        self._assert_new_alg_data(2, 3.75, 0.41, MEMORIZED, alg_data)
        
    def test_schedule_should_do_nothing_if_reviewing_second_time_within_12h(self):
        # when
        old_next_review = datetime.now() + timedelta(4)
        almost_12h_ago = datetime.now() - timedelta(hours=11, minutes=59)
        alg_data = dict(num_reviews=3, avg_grade=3.7, difficulty=2.26,
            last_review=almost_12h_ago, next_review=old_next_review)
        next_review, alg_data = self._algorithm.schedule(grade=0, priority=PRIORITY_LOW, alg_data=alg_data)

        # then
        assert_equals(old_next_review, next_review)
        self._assert_new_alg_data(3, 3.7, 2.26, MEMORIZED, alg_data)

    def test_schedule_consecutive_rep_2_grade(self):
        date_from = date.today() + timedelta(4)
        date_to = date.today() + timedelta(9)
        self._global_data.get_workloads(date_from, date_to, None).AndReturn([63, 40, 33, 20, 18, 50])
        self._global_data.get_avg_difficulties(date_from, date_to, None).AndReturn([6.0, 2.2, 1.5, 1.6, 3.5, 5.1])
        mox.Replay(self._global_data)

        alg_data = dict(num_reviews=3, avg_grade=3.7, difficulty=1.70)
        next_review, alg_data = self._algorithm.schedule(alg_data=alg_data, priority=PRIORITY_LOW, grade=2)

        mox.Verify(self._global_data)
        assert_equals(date.today() + timedelta(8), next_review.date())
        self._assert_new_alg_data(4, 3.28, 3.56, FINAL_DRILL, alg_data)

    def test_schedule_consecutive_rep_3_grade(self):
        date_from = date.today() + timedelta(9)
        date_to = date.today() + timedelta(22)
        num_days = (date_to - date_from).days + 1
        workloads = range(10, 10 + num_days)
        assert_equals(num_days, len(workloads))
        self._global_data.get_workloads(date_from, date_to, None).AndReturn(workloads)
        avg_difficulties = [d / 2.0 for d in range(num_days / 2, 0, -1)] + \
            [d / 2.0 for d in range(num_days / 2, num_days)]
        assert_equals(num_days, len(avg_difficulties))
        self._global_data.get_avg_difficulties(date_from, date_to, None).AndReturn(avg_difficulties)
        mox.Replay(self._global_data)

        alg_data = dict( num_reviews=3, avg_grade=3.7, difficulty=3.36)
        next_review, alg_data = self._algorithm.schedule(alg_data=alg_data, grade=3, priority=PRIORITY_LOW)
        
        mox.Verify(self._global_data)
        assert_equals(date.today() + timedelta(14), next_review.date())
        self._assert_new_alg_data(4, 3.53, 3.04, MEMORIZED,
                                 alg_data)
    
    def test_schedule_consecutive_rep_5_grade(self):
        date_from = date.today() + timedelta(57)
        date_to = date.today() + timedelta(154)
        num_days = (date_to - date_from).days + 1
        workloads = range(num_days, 0, -1)
        assert_equals(num_days, len(workloads))
        self._global_data.get_workloads(date_from, date_to, None).AndReturn(workloads)
        avg_difficulties = [float(d) / num_days for d in range(1, num_days + 1)]
        assert_equals(num_days, len(avg_difficulties))
        self._global_data.get_avg_difficulties(date_from, date_to, None).AndReturn(avg_difficulties)
        mox.Replay(self._global_data)

        alg_data = dict( num_reviews=3, avg_grade=3.7, difficulty=0.41)
        next_review, alg_data = self._algorithm.schedule(grade=5, priority=PRIORITY_LOW, alg_data=alg_data)
        
        mox.Verify(self._global_data)
        assert_equals(date.today() + timedelta(59), next_review.date())
        self._assert_new_alg_data(4, 4.03, 1.66, MEMORIZED,
                                 alg_data)
    
    def test_schedule_consecutive_rep_final_drill_0_grade(self):
        alg_data = dict( num_reviews=2, avg_grade=2.7,
                                       difficulty=0.8, next_review=datetime.now(),
                                       status=FINAL_DRILL)
        next_review, alg_data = self._algorithm.schedule(grade=0, priority=PRIORITY_HIGH, alg_data= alg_data)
        
        self._assert_new_alg_data(2, 2.7, 0.8, FINAL_DRILL,
                                 alg_data)
    
    def test_schedule_consecutive_rep_final_drill_2_grade(self):
        alg_data = dict(num_reviews=2, avg_grade=2.7, difficulty=0.8, next_review=datetime(2001, 10, 10),
                        status=FINAL_DRILL)
        next_review, alg_data = self._algorithm.schedule(grade=2, priority=PRIORITY_HIGH, alg_data=alg_data)

        self.assertEquals(datetime(2001, 10, 10), next_review)
        self._assert_new_alg_data(2, 2.7, 0.8, FINAL_DRILL,
                                 alg_data)

    def test_schedule_consecutive_rep_final_drill_3_grade(self):
        alg_data = dict(num_reviews=2, avg_grade=2.7, difficulty=0.8, next_review=datetime(2001, 10, 10),
                        status=FINAL_DRILL)
        next_review, alg_data = self._algorithm.schedule(grade=3, priority=PRIORITY_HIGH, alg_data=alg_data)

        self.assertEquals(datetime(2001, 10, 10), next_review)
        self._assert_new_alg_data(2, 2.7, 0.8, MEMORIZED,
                                 alg_data)

    def test_schedule_consecutive_rep_final_drill_5_grade(self):
        alg_data = dict(num_reviews=2, avg_grade=2.7, difficulty=0.8, next_review=datetime(2001, 10, 10),
                        status=FINAL_DRILL)
        next_review, alg_data = self._algorithm.schedule(grade=5, priority=PRIORITY_HIGH, alg_data=alg_data)

        self.assertEquals(datetime(2001, 10, 10), next_review)
        self._assert_new_alg_data(2, 2.7, 0.8, MEMORIZED,
                                 alg_data)

    def test_schedule_wrong_alg_data_grade(self):
        alg_data = dict(grade=-1)
        assert_raises(AssertionError, self._algorithm.schedule, alg_data)

        assert_raises(AssertionError, self._algorithm.schedule, 6)
            
    def test_schedule_wrong_alg_data_num_of_reviews(self):
        alg_data = dict(num_reviews=0)
        assert_raises(AssertionError, self._algorithm.schedule, 5, alg_data)
        
    def test_schedule_wrong_alg_data_avg_grade(self):
        alg_data = dict(avg_grade=-0.01)
        assert_raises(AssertionError, self._algorithm.schedule, 5, alg_data)
        
        alg_data = dict(avg_grade=5.01)
        assert_raises(AssertionError, self._algorithm.schedule, 5, alg_data)
        
    def test_schedule_wrong_alg_data_priority(self):
        assert_raises(AssertionError, self._algorithm.schedule, grade=5, priority=-10.0)

        assert_raises(AssertionError, self._algorithm.schedule, grade=5, priority=5.0)

    def test_schedule_wrong_alg_data_difficulty(self):
        alg_data = dict(difficulty=-0.01)
        assert_raises(AssertionError, self._algorithm.schedule, alg_data)

    def test_schedule_wrong_global_data_workloads(self):
        date_from = date.today() + timedelta(3)
        date_to = date.today() + timedelta(7)
        self._global_data.get_workloads(date_from, date_to, None).AndReturn([0, 0, 0, 0])
        mox.Replay(self._global_data)

        assert_raises(AssertionError, self._algorithm.schedule, 5)
        
        mox.Verify(self._global_data)        
    
    def test_schedule_wrong_global_data_avg_difficulties(self):
        date_from = date.today() + timedelta(4)
        date_to = date.today() + timedelta(8)
        self._global_data.get_workloads(date_from, date_to, None).AndReturn([1, 1, 1, 1, 1])
        self._global_data.get_avg_difficulties(date_from, date_to, None).AndReturn([0.0, 0.0, 0.0, 0.0])
        mox.Replay(self._global_data)

        assert_raises(AssertionError, self._algorithm.schedule, 5)
        
        mox.Verify(self._global_data)

    def _assert_interval(self, exp_interval, interval):
        assert_almost_equals(exp_interval, interval, 2)
        
    def _assert_difficulty(self, exp_difficulty, difficulty):
        assert_almost_equals(exp_difficulty, difficulty, 2)
    
    def _assert_load_coeffs(self, exp_load_coeffs, load_coeffs):
        assert_equals(len(exp_load_coeffs), len(load_coeffs))
        for i in range(len(exp_load_coeffs)):
            assert_almost_equals(exp_load_coeffs[i], load_coeffs[i], 3, 
                                    "[%d]: %s != %s within %d places" % (i, exp_load_coeffs[i], load_coeffs[i], 3))
        
    def _assert_new_alg_data(self, exp_num_reviews, exp_avg_grade, exp_difficulty,
                            exp_status, alg_data):
        assert_equals(exp_num_reviews, alg_data['num_reviews'])
        assert_almost_equals(exp_avg_grade, alg_data['avg_grade'], 2)
        self._assert_difficulty(exp_difficulty, alg_data['difficulty'])
        assert_equals(exp_status, alg_data['status'])
