<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useExpenseStore } from '../stores/expenses'

const router = useRouter()
const expenseStore = useExpenseStore()

const expenseGroups = ['Food', 'Transport', 'Entertainment', 'Bills', 'Other']
const group = ref(expenseGroups[0])
const value = ref(0)
const isRecurring = ref(false)

function handleSubmit() {
  expenseStore.addExpense({
    group: group.value,
    value: value.value,
    date: new Date().toISOString(),
    isRecurring: isRecurring.value
  })
  router.push('/')
}
</script>

<template>
  <div class="max-w-2xl mx-auto">
    <div class="bg-white rounded-xl shadow-md p-8">
      <h1 class="text-3xl font-bold mb-8 text-gray-800">New Expense</h1>
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Expense Group</label>
          <select
            v-model="group"
            class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
          >
            <option v-for="group in expenseGroups" :key="group" :value="group">
              {{ group }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Value</label>
          <div class="relative">
            <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">$</span>
            <input
              v-model.number="value"
              type="number"
              step="0.01"
              required
              class="w-full pl-8 pr-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            />
          </div>
        </div>

        <div class="flex items-center">
          <input
            v-model="isRecurring"
            type="checkbox"
            class="h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded transition-colors"
          />
          <label class="ml-3 block text-sm font-medium text-gray-700">Recurring Expense</label>
        </div>

        <div class="flex justify-end space-x-4 pt-4">
          <button
            type="button"
            @click="router.push('/')"
            class="px-6 py-3 bg-gray-100 text-gray-700 font-medium rounded-lg hover:bg-gray-200 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            Save Expense
          </button>
        </div>
      </form>
    </div>
  </div>
</template>