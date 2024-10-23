from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages  # Import messages if you want to show feedback

from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse

class ColorBlindnessTestView(View):
    images = [
        {'image': 'color_blindness_test/images/image_1.jpg', 'answer': '12'},
        {'image': 'color_blindness_test/images/image_2.jpg', 'answer': '8'},
        {'image': 'color_blindness_test/images/image_3.jpg', 'answer': '5'},
        {'image': 'color_blindness_test/images/image_4.jpg', 'answer': 'x'},
        {'image': 'color_blindness_test/images/image_5.jpg', 'answer': 'k'},
        {'image': 'color_blindness_test/images/image_6.jpg', 'answer': 's'},
        {'image': 'color_blindness_test/images/image_7.jpg', 'answer': '26'},
    ]

    def get(self, request):
        current_step = int(request.GET.get('step', 0))
        return render(request, 'color_blindness_test/color_blindness_test.html', {
            'image': self.images[current_step]['image'],
            'step': current_step
        })

    def post(self, request):
        current_step = int(request.POST.get('step', 0))
        user_input = request.POST.get('answer')

        # Store results in the session
        if 'results' not in request.session:
            request.session['results'] = []

        # Append the user input to results
        request.session['results'].append(user_input)

        # Proceed to the next step regardless of the answer
        current_step += 1
        if current_step >= len(self.images):
            return redirect('color_blindness_test_completed')

        return redirect(f'{reverse("color_blindness_test")}?step={current_step}')





class TestCompletedView(TemplateView):
    template_name = 'color_blindness_test/color_blindness_complete.html'

    def get(self, request, *args, **kwargs):
        # Retrieve results from session
        results = request.session.get('results', [])
        # Clear results from session after getting them
        del request.session['results']

        # Determine if user is color blind based on the answers
        correct_answers = ['12', '8', '5']
        is_color_blind = any(result not in correct_answers for result in results)

        # Prepare message to display
        message = "You passed the test. You are not color blind." if not is_color_blind else "You might be color blind. Please consult an eye specialist."

        return render(request, self.template_name, {'message': message})