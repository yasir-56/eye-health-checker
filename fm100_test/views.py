from django.shortcuts import render, redirect
from django.views import View
import time
import random
from django.urls import reverse


COLOR_ROWS = [
    ['#00FF00', '#33FF00', '#66FF00', '#99FF00', '#CCFF00', '#FFFF00', '#FFCC00', '#FF9900', '#FF6600', '#FF3300', '#FF0000'],
    ['#00FF00', '#00FF33', '#00FF66', '#00FF99', '#00FFCC', '#00FFFF', '#0099FF', '#0066FF', '#0033FF', '#0000FF'],
    ['#FF00FF', '#FF33FF', '#FF66FF', '#FF99FF', '#FFCCFF', '#FF00CC', '#FF0099', '#FF0066', '#FF0033', '#FF0000'],
    ['#FF0000', '#FF3333', '#FF6666', '#FF9999', '#FFCCCC', '#FFEEEE', '#FFF0F0', '#FFF5F5', '#FFFAFA'],
]

class FM100TestView(View):
    template_name = 'fm100_test/fm100_test.html'


    def get(self, request):
        shuffled_rows = [row.copy() for row in COLOR_ROWS]
        for row in shuffled_rows:
            random.shuffle(row)
        
        request.session['start_time'] = time.time()
        request.session['correct_order'] = COLOR_ROWS

        return render(request, self.template_name, {
            'rows': shuffled_rows
        })

    def post(self, request):
        start_time = request.session.get('start_time')
        correct_order = request.session.get('correct_order')

        end_time = time.time()
        elapsed_time = round((end_time - start_time) / 60, 2)

        submitted_order = [
            request.POST.getlist('row1[]'),
            request.POST.getlist('row2[]'),
            request.POST.getlist('row3[]'),
            request.POST.getlist('row4[]'),
        ]

        score = self.calculate_score(correct_order, submitted_order)

        # Use reverse to generate the correct URL
        return redirect(reverse('fm100_test_completed', kwargs={'score': score, 'time_taken': elapsed_time}))

    def calculate_score(self, correct_order, submitted_order):
            total_errors = 0
            for correct_row, submitted_row in zip(correct_order, submitted_order):
                for i in range(len(correct_row) - 1):
                    correct_index = correct_row.index(submitted_row[i])
                    next_correct_index = correct_row.index(submitted_row[i+1])
                    if abs(correct_index - next_correct_index) != 1:
                        total_errors += abs(correct_index - next_correct_index) - 1
            return max(0, 100 - total_errors)  # Ensure the score is not negative


class FM100TestCompleteView(View):
    template_name = 'fm100_test/fm100_test_complete.html'

    def get(self, request, score, time_taken):
        return render(request, self.template_name, {
            'score': score,
            'time_taken': time_taken,
            'arrangement': request.session.get('correct_order', COLOR_ROWS),
        })