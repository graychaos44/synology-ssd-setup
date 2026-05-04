# Synology DS925+ 비공식 SSD 등록 스크립트

DSM 7.3.2에서 비공식 NVMe SSD를 호환 DB에 추가하는 스크립트.

## 문제
- 시놀로지는 공식 SSD만 SSD 캐시/볼륨으로 지원
- 비공식 SSD를 끼우면 경고 또는 기능 제한
- 007revad/Synology_HDD_db 스크립트가 DSM 7.3.2 v7 DB에서 parse error 발생

## 해결
- `syno_hdd_db.sh` 대신 직접 Python으로 DB 파일 수정
- v7 DB JSON 파일에 SSD 엔트리 직접 추가

## 환경
- **NAS**: DS925+ (DSM 7.3.2-86009-3)
- **SSD**: Samsung PM9A1 MZVLQ128HBHQ-000 x2 (128GB)
- **HDD**: BarraCuda 1TB (OS), WD 8TB, WD 10TB, HGST 4TB

## 사용법
```bash
ssh admin@<NAS_IP>
sudo python3 add_ssd.py
```

## DB 파일 위치
- `/var.defaults/lib/disk-compatibility/ds925+_host_v7.db`
- `/var/lib/disk-compatibility/ds925+_host_v7.db`

## 주의
- 실행 전 반드시 백업
- DB 수정 후 NAS 재부팅 필요
- DSM 업데이트 시 DB가 초기화될 수 있음
- SSD 캐시가 안 되면 저장 볼륨으로 사용 가능

## 참고
- [007revad/Synology_HDD_db](https://github.com/007revad/Synology_HDD_db) - 원본 스크립트 (DSM 7.3 v7에서 에러)
