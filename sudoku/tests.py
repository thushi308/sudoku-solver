from django.test import TestCase, Client
import json

class SudokuSolverTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.sample_board = [
            5, 3, 0, 0, 7, 0, 0, 0, 0,
            6, 0, 0, 1, 9, 5, 0, 0, 0,
            0, 9, 8, 0, 0, 0, 0, 6, 0,
            8, 0, 0, 0, 6, 0, 0, 0, 3,
            4, 0, 0, 8, 0, 3, 0, 0, 1,
            7, 0, 0, 0, 2, 0, 0, 0, 6,
            0, 6, 0, 0, 0, 0, 2, 8, 0,
            0, 0, 0, 4, 1, 9, 0, 0, 5,
            0, 0, 0, 0, 8, 0, 0, 7, 9
        ]

    def test_index_page_renders(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sudoku Solver')

    def test_solve_via_index_query_param(self):
        response = self.client.get('/', {'board': json.dumps(self.sample_board)})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('solved_board_list', data)
        self.assertEqual(len(data['solved_board_list']), 81)

    def test_solve_endpoint(self):
        response = self.client.get('/solve/', {'board': json.dumps(self.sample_board)})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('solved_board_list', data)
        self.assertEqual(len(data['solved_board_list']), 81)

    def test_solve_without_board(self):
        response = self.client.get('/solve/')
        self.assertEqual(response.status_code, 400)
