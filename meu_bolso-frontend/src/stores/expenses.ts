import { defineStore } from 'pinia'
import { ref } from 'vue'

interface Expense {
  id: number
  group: string
  value: number
  date: string
  isRecurring: boolean
}

export const useExpenseStore = defineStore('expenses', () => {
  const expenses = ref<Expense[]>([])

  function addExpense(expense: Omit<Expense, 'id'>) {
    expenses.value.push({
      ...expense,
      id: Date.now()
    })
  }

  function getExpensesByPeriod(period: 'day' | 'week' | 'month' | 'year') {
    const now = new Date()
    return expenses.value.filter(expense => {
      const expenseDate = new Date(expense.date)
      switch (period) {
        case 'day':
          return expenseDate.toDateString() === now.toDateString()
        case 'week':
          const weekAgo = new Date(now.setDate(now.getDate() - 7))
          return expenseDate >= weekAgo
        case 'month':
          return expenseDate.getMonth() === now.getMonth() &&
                 expenseDate.getFullYear() === now.getFullYear()
        case 'year':
          return expenseDate.getFullYear() === now.getFullYear()
      }
    })
  }

  return { expenses, addExpense, getExpensesByPeriod }
})