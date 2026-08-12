# Generate sample plan-vs-actual chart for the first blog post (fabricated data)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

accounts = ["매출", "매출원가", "판관비", "영업이익"]
plan =   [1200, 780, 260, 160]
actual = [1265, 830, 296, 139]

fig, ax = plt.subplots(figsize=(10, 5.6), dpi=130)
x = range(len(accounts))
w = 0.36
b1 = ax.bar([i - w/2 for i in x], plan, w, label="계획", color="#8fa8c9")
b2 = ax.bar([i + w/2 for i in x], actual, w, label="실적", color="#2e5e94")

for i, (p, a) in enumerate(zip(plan, actual)):
    diff = a - p
    sign = "+" if diff >= 0 else "△"
    color = "#c0392b" if (i in (1, 2) and diff > 0) or (i == 3 and diff < 0) else "#1e7d46"
    ax.annotate(f"{sign}{abs(diff)}", (i + w/2, a), textcoords="offset points",
                xytext=(0, 6), ha="center", fontsize=11, fontweight="bold", color=color)

ax.set_title("월마감 후 과제: 계획 대비 실적 차이 분석 (단위: 백만 원)", fontsize=14, pad=14)
ax.set_xticks(list(x)); ax.set_xticklabels(accounts, fontsize=12)
ax.legend(fontsize=11)
ax.spines[["top", "right"]].set_visible(False)
ax.set_axisbelow(True); ax.grid(axis="y", alpha=0.3)
fig.text(0.99, 0.01, "※ 예시용 가공 데이터입니다", ha="right", fontsize=9, color="#888888")
fig.tight_layout()
out = r"C:\Users\ysmsg\OneDrive\바탕 화면\Google blog\content\assets\2026-06-plan-vs-actual.png"
fig.savefig(out, bbox_inches="tight")
print("saved:", out)
