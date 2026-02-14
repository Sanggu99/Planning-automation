import os

file_path = r"c:\Users\SEOP\Desktop\seop architecture\docs\landscape_quantities.csv"

# The data to write
data_lines = [
    "구분,품명,규격(Specification),수량,단위,비고",
    "교목(Trees),소나무 (Pinus densiflora),H4.0 x R15,150,주,단지 진입부 및 주요 경관 포인트 (상징목)",
    "교목(Trees),느티나무 (Zelkova serrata),R15,120,주,중앙 광장 및 보행로 녹음수",
    "교목(Trees),왕벚나무 (Prunus yedoensis),B12,180,주,순환 산책로 가로수 (봄꽃 명소화)",
    "교목(Trees),단풍나무 (Acer palmatum),R10,90,주,휴게 공간 주변 포인트 식재",
    "교목(Trees),이팝나무 (Chionanthus retusus),R10,110,주,주동 주변 완충 녹지",
    "관목(Shrubs),영산홍 (Rhododendron indicum),H0.3 x W0.3,5000,주,화단 경계 및 군식",
    "관목(Shrubs),회양목 (Buxus microphylla),H0.3 x W0.3,4500,주,생울타리 및 경계 식재",
    "관목(Shrubs),조팝나무 (Spiraea prunifolia),H0.8,3000,주,산책로 주변 자연스러운 경관 연출",
    "지피/초화(Groundcover),한국잔디 (Zoysia japonica),매트,4500,m2,중앙 광장 및 오픈 스페이스",
    "지피/초화(Groundcover),맥문동 (Liriope platyphylla),-,8000,본,수목 하부 그늘 식재",
    "시설물(Facilities),파고라 (Pergola),5000 x 5000,12,개소,주요 휴게 거점",
    "시설물(Facilities),경관 조명 (Landscape Lighting),볼라드 타입,250,개,산책로 및 광장 보행 조명"
]

# Write with utf-8-sig encoding (adds BOM for Excel)
try:
    with open(file_path, 'w', encoding='utf-8-sig') as f:
        f.write('\n'.join(data_lines))
    print(f"Successfully saved {file_path} with utf-8-sig encoding.")
except Exception as e:
    print(f"Error saving file: {e}")
