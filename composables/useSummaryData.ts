import type { SummaryOne } from '@/interfaces'

const CATEGORY_TYPES = {
  income: [100, 101, 110],
  outgoing: [200, 210, 220, 221, 222, 230, 231, 240, 250, 251, 260, 270, 280, 300, 400, 500],
  invest: [700, 701],
} as const

export const useSummaryData = () => {
  const categorizeData = (data: SummaryOne[]) => {
    const income: SummaryOne[] = []
    const outgoing: SummaryOne[] = []
    const invest: SummaryOne[] = []

    for (const item of data) {
      if (CATEGORY_TYPES.income.includes(item.category_id)) {
        income.push(item)
      }
      else if (CATEGORY_TYPES.outgoing.includes(item.category_id)) {
        outgoing.push(item)
      }
      else if (CATEGORY_TYPES.invest.includes(item.category_id)) {
        invest.push(item)
      }
    }

    return { income, outgoing, invest }
  }

  const calculateSum = (data: SummaryOne[], categoryName: string): SummaryOne => {
    const sumData: SummaryOne = {
      category_id: 999,
      category_name: categoryName,
      price: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      total: 0,
    }

    for (const item of data) {
      for (let i = 0; i < 12; i++) {
        sumData.price[i] += item.price[i]
      }
      sumData.total += item.total
    }

    return sumData
  }

  const calculateNetSum = (
    incomeSum: SummaryOne,
    outgoingSum: SummaryOne,
    investSum: SummaryOne,
    includeInvestment = true,
  ): SummaryOne => {
    const netSum: SummaryOne = {
      category_id: 999,
      category_name: includeInvestment ? '合計' : '合計（投資除く）',
      price: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      total: 0,
    }

    for (let i = 0; i < 12; i++) {
      netSum.price[i] = incomeSum.price[i] - outgoingSum.price[i]
      if (includeInvestment) {
        netSum.price[i] -= investSum.price[i]
      }
    }

    netSum.total = incomeSum.total - outgoingSum.total
    if (includeInvestment) {
      netSum.total -= investSum.total
    }

    return netSum
  }

  return {
    categorizeData,
    calculateSum,
    calculateNetSum,
  }
}
