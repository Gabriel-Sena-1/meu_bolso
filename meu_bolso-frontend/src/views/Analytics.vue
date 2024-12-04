<script setup lang="ts">
import { ref, computed } from 'vue'
import { useExpenseStore } from '../stores/expenses'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

const expenseStore = useExpenseStore()
const selectedPeriod = ref('month')

const chartData = computed(() => {
  const expenses = expenseStore.getExpensesByPeriod(selectedPeriod.value)
  const groupedExpenses = expenses.reduce((acc, expense) => {
    if (!acc[expense.group]) {
      acc[expense.group] = 0
    }
    acc[expense.group] += expense.value
    return acc
  }, {})

  return {
    labels: Object.keys(groupedExpenses),
    datasets: [{
      label: 'Expenses by Group',
      data: Object.values(groupedExpenses),
      borderColor: 'rgb(59, 130, 246)',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      borderWidth: 2,
      tension: 0.4,
      fill: true
    }]
  }
})
</script>

<template>
  <div class="space-y-8">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <h1 class="text-3xl font-bold text-gray-800">Expense Analytics</h1>
      <select
        v-model="selectedPeriod"
        class="px-4 py-2 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
      >
        <option value="day">Today</option>
        <option value="week">This Week</option>
        <option value="month">This Month</option>
        <option value="year">This Year</option>
      </select>
    </div>

    <div class="bg-white p-6 rounded-xl shadow-md">
      <Line 
        :data="chartData" 
        :options="{ 
          responsive: true,
          plugins: {
            legend: {
              position: 'top'
            }
          }
        }" 
      />
    </div>
  </div>
</template>