# This file is for strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits


class Bot(GoslingAgent):
    # This function runs every in-game tick (every time the game updates anything)
    def run(self):
        if self.intent is not None:
            return
        d1 = abs(self.ball.location.y - self.foe_goal.location.y)
        d2 = abs(self.me.location.y - self.foe_goal.location.y)
        is_in_front_of_ball = d1 > d2
        if self.kickoff_flag:
            self.set_intent(kickoff())
            return
        # So... I'm just not going to refactor this because I don't want to delete something I need, or vice versa, leave something I don't need.
        if is_in_front_of_ball:
            self.set_intent(goto(self.friend_goal.location))
            return
        self.set_intent(short_shot(self.foe_goal.location))

        targets = {
            'at_opponent_goal': (self.foe_goal.left_post, self.foe_goal.right_post),
            'away_from_our_net': (self.friend_goal.right_post, self.friend_goal.left_post)
        }
        hits = find_hits(self,targets)
        if len(hits['at_opponent_goal']) > 0:
            self.set_intent(hits['at_opponent_goal'][0])
            return
        if len(hits['away_from_our_net']) > 0:
            self.set_intent(hits['away_from_our_net'][0])
            return
        
        available_boosts = [boost for boost in self.boosts if boost.large and boost.active]
        if len(available_boosts) > 0:
            self.set_intent(goto(available_boosts[0].location))
            print('going for boosts', available_boosts[0].index)
            return

        if self.me.boost > 99:
            self.set_intent(short_shot(self.foe_goal.location))
            return

        closest_boost = self.get_closest_large_boost()
 
        if closest_boost is not None:
            self.set_intent(goto(closest_boost.location))
            return