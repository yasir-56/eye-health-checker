from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
import random
from urllib.parse import quote, unquote
# Create your views here.


LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
SIZES = [200, 100, 50, 25, 12, 6]  # Font sizes in pixels

class EyeSightTestView(View):
    template_name = 'eye_sight_test/eye_sight_test.html'

    def get(self, request):
        letters = [random.choice(LETTERS) for _ in range(len(SIZES))]
        request.session['test_letters'] = letters
        return render(request, self.template_name, {'letters': zip(letters, SIZES)})

    def post(self, request):
        correct_letters = request.session.get('test_letters', [])
        user_answers = [request.POST.get(f'letter_{i}', '').upper() for i in range(len(SIZES))]

        score = sum(1 for correct, user in zip(correct_letters, user_answers) if correct == user)
        visual_acuity = self.calculate_visual_acuity(score)

        # Encode the visual_acuity value
        encoded_visual_acuity = quote(visual_acuity)

        return redirect(reverse('eye_sight_test_completed', kwargs={'score': score, 'visual_acuity': encoded_visual_acuity}))

    def calculate_visual_acuity(self, score):
        if score == 6:
            return "20,20"
        elif score == 5:
            return "20,30"
        elif score == 4:
            return "20,40"
        elif score == 3:
            return "20,50"
        elif score == 2:
            return "20,70"
        elif score == 1:
            return "20,100"
        else:
            return "20,200 or worse"



class EyeSightTestCompleteView(View):
    template_name = 'eye_sight_test/eye_sight_test_complete.html'

    def get(self, request, score, visual_acuity):
        # Decode the visual_acuity value
        decoded_visual_acuity = unquote(visual_acuity)
        return render(request, self.template_name, {
            'score': score,
            'visual_acuity': decoded_visual_acuity,
        })