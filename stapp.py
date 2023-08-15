# examples for few-shot prompt templating
examples = [
  {
    "training_start_date": "July 26",  
    "marathon_date": "Dec 20",
    "pd_run_output": "The average distance is 3.71 miles and the maximum distance is 9.52 miles. The average moving time is not available and the maximum moving time is not available. Other running statistics include total elevation gain, with an average of 47.6 and a maximum of 200.6.",
    "num_workouts": "147",
    "plan": 
"""
Good luck on {marathon_date}. 
Week 1: 
Day 1, {training_start_date}: tennis for 1 hour
Day 2: 4 miles easy run 
Day 3: 3 miles easy run 
Day 4: 5 miles easy run 
Day 5: bike for 45 minutes
Day 6: 6 miles easy run 
Day 7: 4 miles easy run 
Week 2: 
Day 8: swim for 30 minutes 
Day 9: 4 miles easy run 
Day 10: 3 miles easy run 
Day 11: 6 miles easy run 
Day 12: tennis for 1.5 hours 
Day 13: 7 miles easy run 
Day 14: 4 miles easy run 
Week 3: 
Day 15: tennis for an hour 
Day 16: 5 miles easy run 
Day 17: 4 miles easy run 
Day 18: 7 miles easy run 
Day 19: swim for 30 minutes 
Day 20: Long run - 8 miles at an easy pace
Day 21: 4 miles easy run 
Week 4: 
Day 22: bike 8 miles 
Day 23: 5 miles easy run 
Day 24: 4 miles easy run 
Day 25: 8 miles easy run 
Day 26: bike 10 miles 
Day 27: Long run - 9 miles at an easy pace 
Day 28: 4 miles easy run 
Week 5:
Day 29: tennis for an hour and a half 
Day 30: 9 miles easy run
Day 31: 4 miles easy run 
Day 32: 6 miles easy run
Day 33: tennis match
Day 34: Long run - 10 miles at an easy pace
Day 35: 4 miles easy run 
Week 6: 
Day 36: bike ride to and from Golden Gate Park (8 miles) 
Day 37: Long run - 10 miles at an easy pace 
Day 38: 4 miles easy run 
Day 39: 6 miles easy run
Day 40: tennis for an hour 
Day 41: 4 miles easy run
Day 42: Long run - 11 miles easy run
Week 7: 
Day 43: tennis for an hour and a half 
Day 44: Long run - 11 miles at an easy pace
Day 45: 4 miles easy run 
Day 46: 7 miles easy run 
Day 47: tennis for an hour 
Day 48: 4 miles easy run
Day 49: Long run - 12 miles at an easy pace
Week 8: 
Day 50: swim for 30 minutes 
Day 51: Long run - 12 miles at an easy pace
Day 52: 4 miles easy run
Day 53: 7 miles easy run
Day 54: tennis for 1.5 hours 
Day 55: 4 miles easy run
Day 56: Long run - 13 miles at an easy pace 
Week 9: 
Day 57: swim for 30 minutes 
Day 58: Long run - 10 miles easy run
Day 59: 4 miles easy run
Day 60: 8 miles easy run
Day 61: bike for 1 hour 
Day 62: Long run - 14 miles at an easy pace
Day 63: 4 miles easy run
Week 10: 
Day 64: swim for 30 minutes  
Day 65: Long run - 11 miles easy run 
Day 66: 4 miles easy run 
Day 67: 7 miles easy run
Day 68: tennis for 1 hour 
Day 69: Long run - 15 miles easy run 
Day 70: 4 miles easy run 
Week 11: 
Day 71: tennis for 1 hour 
Day 72: Long run - 10 miles at an easy pace 
Day 73: 4 miles easy run 
Day 74: 8 miles easy run
Day 75: tennis for 1 hour 
Day 76: Long run - 16 miles easy run 
Day 77: 4 miles easy run 
Week 12: 
Day 78: swim for 30 minutes 
Day 79: Long run - 10 miles at an easy pace 
Day 80: 4 miles medium run 
Day 81: 9 miles easy run 
Day 82: swim for 30 minutes 
Day 83: Long run - 17 miles at an easy pace 
Day 84: 4 miles easy run 
Week 13: 
Day 85: tennis for 1 hour 
Day 86: Long run - 10 miles easy run
Day 87: 4 miles easy run 
Day 88: 8 miles easy run
Day 89: bike ride for 45 minutes 
Day 90: Long run - 18 miles at an easy pace
Day 91: 4 miles easy run 
Week 14: 
Day 92: tennis for 1 hour 
Day 93: 12 miles easy run 
Day 94: 4 miles medium run 
Day 95: 10 miles easy run 
Day 96: swim for 30 minutes 
Day 97: Long run - 19 miles at an easy pace 
Day 98: 3 miles sprint intervals 
Week 15: 
Day 99: tennis for 1 hour 
Day 100: Long run - 11 miles easy run 
Day 101: 4 miles easy run 
Day 102: 10 miles easy run 
Day 103: tennis for 1 hour 
Day 104: Long run - 20 miles at an easy pace 
Day 105: 4 miles easy run 
Week 16: 
Day 106: swim for 30 minutes 
Day 107: 9 miles easy run 
Day 108: 9 miles easy run 
Day 109: 9 miles easy run 
Day 110: tennis for 1 hour 
Day 111: Long run - 17 miles easy run 
Day 112: 4 miles easy run 
Week 17: 
Day 113: tennis for 1.5 hours 
Day 114: 10 miles easy run 
Day 115: 4 miles easy run 
Day 116: 10 miles easy run 
Day 117: bike ride for 45 minutes 
Day 118: Long run - 18 miles at an easy pace 
Day 119: 4 miles easy run 
Week 18: 
Day 120: tennis for 1 hour 
Day 121: 10 miles easy run 
Day 122: 10 miles easy run 
Day 123: 9 miles easy run 
Day 124: tennis for 1 hour 
Day 125: Long run - 16 miles at an easy pace 
Day 126: 4 miles easy run 
Week 19: 
Day 127: tennis for 1 hour 
Day 128: 11 miles easy run 
Day 129: 8 miles easy run 
Day 130: 10 miles easy run 
Day 131: tennis for 1 hour 
Day 132: Long run - 17 miles at an easy pace 
Day 133: 4 miles easy run 
Week 20: 
Day 134: swim for 20 minutes 
Day 135: 10 miles easy run 
Day 136: 9 miles easy run 
Day 137: 11 miles easy run 
Day 138: bike for 30 minutes 
Day 139: Long run - 18 miles at an easy pace 
Day 140: 4 miles easy run 
Week 21: 
Day 141: tennis for 1 hour 
Day 142: 7 miles easy run 
Day 143: 9 miles easy run 
Day 144: 10 miles easy run 
Day 145: swim for 20 minutes 
Day 146: Rest
Day 147: Rest 
{marathon_date}: Marathon Day!
"""
  },
  {
    "training_start_date" : "July 19",
    "marathon_date" : "November 8",
    "pd_run_output": "The average distance is 3.71 miles and the maximum distance is 9.52 miles. The average moving time is not available and the maximum moving time is not available. Other running statistics include total elevation gain, with an average of 47.6 and a maximum of 200.6.",
    "num_workouts": "112",
    "plan": 
"""
Week 1: 
Day 1, {training_start_date}: Cross-training - Swim
Day 2: Easy run - 4 miles at an easy pace
Day 3: Cross-training - Elliptical 
Day 4: Medium run - 5 miles at a medium pace 
Day 5: Cross-training - Weight Training
Day 6: Long run - 6 miles at an easy pace 
Day 7: Rest day 
Week 2: 
Day 8: Easy run - 4 miles at an easy pace
Day 9: Cross-training - Ride 
Day 10: Medium run - 5 miles at a medium pace 
Day 11:Cross-training - Swim 
Day 12: Long run - 7 miles at an easy pace 
Day 13: Rest day 
Day 14: Sprint workout - 3 miles at a hard pace 
Week 3: 
Day 15: Easy run - 4 miles at an easy pace 
Day 16: Cross-training - Bike ride 
Day 17: Medium run - 6 miles at a medium pace 
Day 18: Cross-training - Elliptical 
Day 19: Long run - 8 miles at an easy pace 
Day 20: Rest day 
Day 21: Sprint workout - 3 miles at a hard pace 
Week 4: 
Day 22: Easy run - 5 miles at an easy pace 
Day 23: Cross-training - Ride
Day 24: Medium run - 6 miles at a medium pace 
Day 25: Cross-training - Weight Training 
Day 26: Long run - 9 miles at an easy pace 
Day 27: Rest day 
Day 28: Sprint workout - 4 miles at a hard pace
Week 5: 
Day 29: Easy run - 5 miles at an easy pace 
Day 30: Cross-training - Swim 
Day 31: Medium run - 7 miles at a medium pace 
Day 32: Cross-training - Walk 
Day 33: Long run - 10 miles at an easy pace 
Day 34: Rest day 
Day 35: Sprint workout - 4 miles at a hard pace 
Week 6: 
Day 36: Easy run - 5 miles at an easy pace 
Day 37: Cross-training - Elliptical 
Day 38: Medium run - 7 miles at a medium pace 
Day 39: Cross-training - Ride 
Day 40: Long run - 11 miles at an easy pace 
Day 41: Rest day 
Day 42: Sprint workout - 5 miles at a hard pace 
Week 7: 
Day 43: Easy run - 6 miles at an easy pace
Day 44: Cross-training - Weight Training 
Day 45: Medium run - 8 miles at a medium pace 
Day 46: Cross-training - Swim 
Day 47: Long run - 12 miles at an easy pace 
Day 48: Rest day 
Day 49: Sprint workout - 5 miles at a hard pace 
Week 8: 
Day 50: Easy run - 6 miles at an easy pace 
Day 51: Cross-training - Walk 
Day 52: Medium run - 8 miles at a medium pace 
Day 53: Cross-training - Elliptical 
Day 54: Long run - 13 miles at an easy pace 
Day 55: Rest day 
Day 56: Sprint workout - 6 miles at a hard pace 
Week 9: 
Day 57: Easy run - 6 miles at an easy pace 
Day 58: Cross-training - Ride 
Day 59: Medium run - 9 miles at a medium pace 
Day 60: Cross-training - Weight Training 
Day 61: Long run - 14 miles at an easy pace 
Day 62: Rest day 
Day 63: Sprint workout - 6 miles at a hard pace
Week 10: 
Day 64: Easy run - 7 miles at an easy pace 
Day 65: Cross-training - Swim 
Day 66: Medium run - 9 miles at a medium pace 
Day 67: Cross-training - Walk 
Day 68: Long run - 14 miles at an easy pace 
Day 69: Rest day 
Day 70: Sprint workout - intervals 
Week 11: 
Day 71: Easy run - 7 miles at an easy pace 
Day 72: Cross-training - Elliptical and Weight Training
Day 73: Medium run - 10 miles at a medium pace 
Day 74: Cross-training - Ride 
Day 75: Long run - 14 miles at an easy pace 
Day 76: Rest day 
Day 77: Sprint workout - intervals
Week 12: 
Day 78: Easy run - 7 miles at an easy pace
Day 79: Cross-training - Elliptical and Weight Training 
Day 80: Medium run - 10 miles at a medium pace 
Day 81: Cross-training - Swim 
Day 82: Long run - 15 miles at an easy pace 
Day 83: Rest day 
Day 84: Sprint workout - intervals 
Week 13: 
Day 85: Easy run - 8 miles at an easy pace 
Day 86: Cross-training - Walk 
Day 87: Medium run - 11 miles at a medium pace 
Day 88: Cross-training - Elliptical and Weight Training
Day 89: Long run - 16 miles at an easy pace 
Day 90: Rest day 
Day 91: Sprint workout - 1 mile at a hard pace 
Week 14: 
Day 92: Easy run - 8 miles at an easy pace 
Day 93: Cross-training - Ride 
Day 94: Medium run - 11 miles at a medium pace 
Day 95: Cross-training - Weight Training 
Day 96: Long run - 17 miles at an easy pace 
Day 97: Rest day 
Day 98: Sprint workout - 1 mile at a hard pace
Week 15: 
Day 99: Easy run - 8 miles at an easy pace 
Day 100: Cross-training - Swim 
Day 101: Medium run - 10 miles at a medium pace 
Day 102: Cross-training - bike ride 
Day 103: Long run - 18 miles at an easy pace 
Day 104: Rest day 
Day 105: Sprint workout intervals 
Week 16:
Day 106: Easy run - 8 miles at an easy pace  
Day 107: Cross-training - Tennis
Day 108: Medium run - 11 miles at a medium pace
Day 109: Cross-training - Elliptical and Weight Training
Day 110: Easy run - 8 miles at an easy pace 
Day 111: Rest day 
Day 112: Rest day
{marathon_date}: Marathon Day!
Note: The above plan assumes that the student is currently able to comfortably run 4 miles at an easy pace. Adjustments may need
to be made if the student is not yet at this level. Additionally, the plan includes cross-training and rest days to
ensure proper recovery and prevent injury.
"""
  }
]