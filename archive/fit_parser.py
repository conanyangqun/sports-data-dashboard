import fitdecode
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import os


@dataclass
class RecordData:
    timestamp: Optional[datetime] = None
    position_lat: Optional[float] = None
    position_long: Optional[float] = None
    altitude: Optional[float] = None
    distance: Optional[float] = None
    speed: Optional[float] = None
    heart_rate: Optional[int] = None
    cadence: Optional[int] = None
    power: Optional[int] = None
    temperature: Optional[int] = None


@dataclass
class LapData:
    start_time: Optional[datetime] = None
    total_elapsed_time: Optional[float] = None
    total_timer_time: Optional[float] = None
    total_distance: Optional[float] = None
    avg_speed: Optional[float] = None
    max_speed: Optional[float] = None
    avg_heart_rate: Optional[int] = None
    max_heart_rate: Optional[int] = None
    avg_cadence: Optional[int] = None
    avg_power: Optional[int] = None
    max_power: Optional[int] = None
    total_calories: Optional[int] = None


@dataclass
class SessionData:
    sport: Optional[str] = None
    sub_sport: Optional[str] = None
    start_time: Optional[datetime] = None
    total_elapsed_time: Optional[float] = None
    total_distance: Optional[float] = None
    avg_speed: Optional[float] = None
    max_speed: Optional[float] = None
    avg_heart_rate: Optional[int] = None
    max_heart_rate: Optional[int] = None
    avg_cadence: Optional[int] = None
    avg_power: Optional[int] = None
    max_power: Optional[int] = None
    total_calories: Optional[int] = None


@dataclass
class ActivityData:
    timestamp: Optional[datetime] = None
    sport: Optional[str] = None
    records: list = field(default_factory=list)
    laps: list = field(default_factory=list)
    sessions: list = field(default_factory=list)


class FITParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.activity = ActivityData()

    def parse(self) -> ActivityData:
        with fitdecode.FitReader(self.file_path) as fit:
            for frame in fit:
                if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                    self._process_frame(frame)
        return self.activity

    def _process_frame(self, frame):
        name = frame.name
        fields = frame.fields

        if name == 'activity':
            self.activity.timestamp = self._get_field_value(fields, 'timestamp')
            sport_val = self._get_field_value(fields, 'sport')
            self.activity.sport = self._sport_value_to_str(sport_val)

        elif name == 'session':
            session = SessionData(
                sport=self._sport_value_to_str(self._get_field_value(fields, 'sport')),
                sub_sport=self._get_field_value(fields, 'sub_sport'),
                start_time=self._get_field_value(fields, 'start_time'),
                total_elapsed_time=self._get_field_value(fields, 'total_elapsed_time'),
                total_distance=self._get_field_value(fields, 'total_distance'),
                avg_speed=self._get_field_value(fields, 'avg_speed'),
                max_speed=self._get_field_value(fields, 'max_speed'),
                avg_heart_rate=self._get_field_value(fields, 'avg_heart_rate'),
                max_heart_rate=self._get_field_value(fields, 'max_heart_rate'),
                avg_cadence=self._get_field_value(fields, 'avg_cadence'),
                avg_power=self._get_field_value(fields, 'avg_power'),
                max_power=self._get_field_value(fields, 'max_power'),
                total_calories=self._get_field_value(fields, 'total_calories'),
            )
            self.activity.sessions.append(session)

        elif name == 'lap':
            lap = LapData(
                start_time=self._get_field_value(fields, 'start_time'),
                total_elapsed_time=self._get_field_value(fields, 'total_elapsed_time'),
                total_timer_time=self._get_field_value(fields, 'total_timer_time'),
                total_distance=self._get_field_value(fields, 'total_distance'),
                avg_speed=self._get_field_value(fields, 'avg_speed'),
                max_speed=self._get_field_value(fields, 'max_speed'),
                avg_heart_rate=self._get_field_value(fields, 'avg_heart_rate'),
                max_heart_rate=self._get_field_value(fields, 'max_heart_rate'),
                avg_cadence=self._get_field_value(fields, 'avg_cadence'),
                avg_power=self._get_field_value(fields, 'avg_power'),
                max_power=self._get_field_value(fields, 'max_power'),
                total_calories=self._get_field_value(fields, 'total_calories'),
            )
            self.activity.laps.append(lap)

        elif name == 'record':
            lat = self._get_field_value(fields, 'position_lat')
            lon = self._get_field_value(fields, 'position_long')
            if lat is not None:
                lat = lat * (180 / 2**31)
            if lon is not None:
                lon = lon * (180 / 2**31)

            record = RecordData(
                timestamp=self._get_field_value(fields, 'timestamp'),
                position_lat=lat,
                position_long=lon,
                altitude=self._get_field_value(fields, 'altitude'),
                distance=self._get_field_value(fields, 'distance'),
                speed=self._get_field_value(fields, 'speed'),
                heart_rate=self._get_field_value(fields, 'heart_rate'),
                cadence=self._get_field_value(fields, 'cadence'),
                power=self._get_field_value(fields, 'power'),
                temperature=self._get_field_value(fields, 'temperature'),
            )
            self.activity.records.append(record)

    def _get_field_value(self, fields, field_name):
        for f in fields:
            if f.name == field_name:
                return f.value
        return None

    def _sport_value_to_str(self, value):
        sport_map = {
            0: 'generic',
            1: 'running',
            2: 'cycling',
            3: 'transition',
            4: 'fitness_equipment',
            5: 'swimming',
            6: 'basketball',
            7: 'soccer',
            8: 'tennis',
            9: 'american_football',
            10: 'walking',
            11: 'cross_country_skiing',
            12: 'alpine_skiing',
            13: 'snowboarding',
            14: 'rowing',
            15: 'mountaineering',
            16: 'hiking',
            17: 'multisport',
            18: 'paddle',
            19: 'flying',
            20: 'e_bike',
            21: 'motorcycling',
            22: 'boating',
            23: 'golf',
            24: 'hang_gliding',
            25: ' horseback_riding',
            26: 'hunting',
            27: 'fishing',
            28: 'inline_skating',
            29: 'rock_climbing',
            30: 'workout',
            31: 'whitewater',
            32: 'sailing',
            33: 'winter_sports',
            34: 'windsurfing',
            35: 'kitesurfing',
            36: 'ballet',
            37: 'preparing_for_a_comp',
            38: 'martial_arts',
            39: 'gymnastics',
            40: 'dance',
            41: 'yoga',
            42: 'boxing',
            43: 'indoor_cycling',
            44: 'indoor_running',
            45: 'equestrian_sports',
            46: 'archery',
            47: 'volleyball',
            48: 'softball',
            49: 'badminton',
            50: 'squash',
            51: 'table_tennis',
            52: 'fencing',
            53: 'beach_soccer',
            54: 'beach_volleyball',
            55: 'bowling',
            56: 'lawn_bowls',
            57: 'curling',
            58: 'snow_sports',
            59: 'lacrosse',
            60: 'rugby',
            61: 'skiing',
            62: 'speed_walking',
            63: 'football',
            64: 'darts',
            65: 'shooting',
            66: 'martial_arts',
            67: 'rowing',
            68: 'badminton',
            69: 'hockey',
            70: 'handball',
            71: 'indoor_climbing',
            72: 'bouldering',
            73: "surfing",
            74: "wakeboarding",
            75: "waterskiing",
            76: "tubes",
            77: "kneeboarding",
            78: "wakesurfing",
            79: "weightlifting",
            80: "track_cycling",
            81: "indoor_rower",
            82: "stair_climbing",
            82: "stair_stepping",
            83: "rope_jumping",
            84: "stretching",
            85: "cross_training",
            86: "planking",
            87: "indoor_skiing",
            88: "viral_video",
            85: "yoga",
        }
        return sport_map.get(value, f'unknown_{value}') if value is not None else None


def print_activity_summary(activity: ActivityData):
    print(f"{'='*60}")
    print(f"FIT 文件解析结果")
    print(f"{'='*60}")

    if activity.timestamp:
        print(f"\n活动开始时间: {activity.timestamp}")
    if activity.sport:
        print(f"运动类型: {activity.sport}")

    print(f"\n记录点数: {len(activity.records)}")
    print(f"圈数: {len(activity.laps)}")
    print(f"会话: {len(activity.sessions)}")

    if activity.sessions:
        print(f"\n{'='*60}")
        print("会话汇总:")
        for i, session in enumerate(activity.sessions, 1):
            print(f"\n  会话 {i}:")
            if session.total_elapsed_time:
                print(f"    总时间: {session.total_elapsed_time:.2f} 秒")
            if session.total_distance:
                print(f"    总距离: {session.total_distance:.2f} 米")
            if session.avg_speed:
                print(f"    平均速度: {session.avg_speed:.2f} m/s")
            if session.max_speed:
                print(f"    最大速度: {session.max_speed:.2f} m/s")
            if session.avg_heart_rate:
                print(f"    平均心率: {session.avg_heart_rate} bpm")
            if session.max_heart_rate:
                print(f"    最大心率: {session.max_heart_rate} bpm")
            if session.avg_cadence:
                print(f"    平均踏频: {session.avg_cadence} rpm")
            if session.avg_power:
                print(f"    平均功率: {session.avg_power} W")
            if session.max_power:
                print(f"    最大功率: {session.max_power} W")
            if session.total_calories:
                print(f"    总卡路里: {session.total_calories} kcal")

    if activity.laps:
        print(f"\n{'='*60}")
        print("圈数汇总:")
        for i, lap in enumerate(activity.laps, 1):
            print(f"\n  圈 {i}:")
            if lap.start_time:
                print(f"    开始时间: {lap.start_time}")
            if lap.total_elapsed_time:
                print(f"    耗时: {lap.total_elapsed_time:.2f} 秒")
            if lap.total_distance:
                print(f"    距离: {lap.total_distance:.2f} 米")
            if lap.avg_speed:
                print(f"    平均速度: {lap.avg_speed:.2f} m/s")
            if lap.max_speed:
                print(f"    最大速度: {lap.max_speed:.2f} m/s")
            if lap.avg_heart_rate:
                print(f"    平均心率: {lap.avg_heart_rate} bpm")
            if lap.max_heart_rate:
                print(f"    最大心率: {lap.max_heart_rate} bpm")
            if lap.avg_power:
                print(f"    平均功率: {lap.avg_power} W")
            if lap.total_calories:
                print(f"    卡路里: {lap.total_calories} kcal")

    if activity.records:
        print(f"\n{'='*60}")
        print("前10条记录数据:")
        for i, record in enumerate(activity.records[:10], 1):
            print(f"\n  记录 {i}:")
            if record.timestamp:
                print(f"    时间: {record.timestamp}")
            if record.position_lat and record.position_long:
                print(f"    位置: {record.position_lat:.6f}, {record.position_long:.6f}")
            if record.altitude:
                print(f"    海拔: {record.altitude:.1f} 米")
            if record.distance:
                print(f"    距离: {record.distance:.2f} 米")
            if record.speed:
                print(f"    速度: {record.speed:.2f} m/s")
            if record.heart_rate:
                print(f"    心率: {record.heart_rate} bpm")
            if record.cadence:
                print(f"    踏频: {record.cadence} rpm")
            if record.power:
                print(f"    功率: {record.power} W")
            if record.temperature:
                print(f"    温度: {record.temperature}°C")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("用法: python fit_parser.py <fit文件路径>")
        print("示例: python fit_parser.py activity.fit")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"错误: 文件不存在 - {file_path}")
        sys.exit(1)

    print(f"正在解析文件: {file_path}")

    try:
        parser = FITParser(file_path)
        activity = parser.parse()
        print_activity_summary(activity)
    except Exception as e:
        print(f"解析错误: {e}")
        import traceback
        traceback.print_exc()
