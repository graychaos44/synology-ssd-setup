# Synology DS925+ 비공식 SSD 등록 스크립트

DSM 7.3.2에서 비공식 NVMe SSD를 호환 DB에 추가하는 스크립트.

## 문제
- 시놀로지는 공식 SSD만 SSD 캐시/볼륨으로 지원
- 비공식 SSD를 끼우면 경고 또는 기능 제한
- [007revad/Synology_HDD_db](https://github.com/007revad/Synology_HDD_db) 스크립트가 DSM 7.3.2 v7 DB에서 parse error 발생

## 해결
- `syno_hdd_db.sh` 대신 직접 Python으로 DB 파일 수정
- v7 DB JSON 파일에 SSD 엔트리 직접 추가

## 테스트 환경
- **NAS**: DS925+ (DSM 7.3.2-86009-3)
- **SSD**: Samsung PM9A1 MZVLQ128HBHQ-000 x2 (128GB, FW: FXV70K0Q)
- **결과**: SSD 캐시는 불가, 저장 볼륨(RAID0)으로 사용 가능

## 사용법
```bash
ssh admin@<NAS_IP>
sudo python3 add_ssd.py
```

## DB 파일 위치
- `/var.defaults/lib/disk-compatibility/ds925+_host_v7.db`
- `/var/lib/disk-compatibility/ds925+_host_v7.db`

## 추가된 SSD 엔트리
```json
{
  "SAMSUNG MZVLQ128HBHQ-000": {
    "FXV70K0Q": {
      "size_gb": 128,
      "compatibility_interval": [
        {
          "compatibility": "compatible",
          "not_after": "",
          "fw_dsm_update_status": "not_required",
          "not_before": ""
        }
      ],
      "support_m2_volume": true,
      "support_ssd_cache": true,
      "support_trim": true
    }
  }
}
```

## NAS 스토리지 벤치마크

| 볼륨 | 드라이브 | 용량 | 쓰기 | 읽기 |
|---|---|---|---|---|
| volume4 | Samsung PM9A1 x2 RAID0 | 256GB | 773 MB/s | 1,400 MB/s |
| volume1 | BarraCuda SATA SSD | 1TB | 496 MB/s | 543 MB/s |
| volume5 | WD 8TB HDD | 8TB | 234 MB/s | 215 MB/s |
| volume2 | HGST 4TB HDD | 4TB | 114 MB/s | 126 MB/s |
| volume3 | WD 8+10TB HDD | 18TB | 98 MB/s | 127 MB/s |

## 주의
- 실행 전 반드시 백업 (스크립트가 자동으로 .bak 생성)
- DB 수정 후 NAS 재부팅 필요
- DSM 업데이트 시 DB가 초기화될 수 있음
- SSD 캐시가 안 되면 저장 볼륨으로 사용 가능 (우리 경우 RAID0 볼륨4로 사용)

## 복원
```bash
sudo python3 restore.py
```

## 참고
- [007revad/Synology_HDD_db](https://github.com/007revad/Synology_HDD_db) - 원본 스크립트 (DSM 7.3 v7에서 에러)
- [이슈 #514](https://github.com/007revad/Synology_HDD_db/issues/514) - DSM 7.3 관련 논의
