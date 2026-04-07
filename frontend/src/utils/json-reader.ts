/**
 * JSON 数据读取模块
 * 从 /data/data.json 文件读取数据
 */

export interface UserData {
  id: number
  username: string
  display_name?: string
  avatar_url: string
  bio: string
}

export interface ActivityData {
  id: number
  activity_type: string
  start_time: string
  duration: number | null
  distance: number | null
  calories: number | null
  max_speed: number | null
  avg_speed: number | null
  max_heart_rate: number | null
  avg_heart_rate: number | null
  max_cadence: number | null
  avg_cadence: number | null
  max_power: number | null
  avg_power: number | null
  normalized_power: number | null
  elevation_gain: number | null
}

export interface DataFile {
  user: UserData | null
  activities: ActivityData[]
}

/**
 * 加载完整的 JSON 数据
 */
export async function loadData(): Promise<DataFile> {
  try {
    const response = await fetch(`${import.meta.env.BASE_URL}data/data.json`)
    if (!response.ok) {
      throw new Error('Failed to load data file')
    }
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error loading data:', error)
    // 返回空数据结构
    return {
      user: null,
      activities: []
    }
  }
}

/**
 * 获取所有运动数据
 */
export async function getActivities(): Promise<ActivityData[]> {
  const data = await loadData()
  return data.activities || []
}

/**
 * 获取用户信息
 */
export async function getUser(): Promise<UserData | null> {
  const data = await loadData()
  return data.user || null
}
