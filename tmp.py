import numpy as np
from scipy.stats import pearsonr
from sklearn.metrics import r2_score

# 加载npy文件
y_true = np.load('/home/lenovo/yinzhou/Time-Series-Library/results/long_term_forecast_custom_timesnet_TimesNet_custom_ftMS_sl256_ll128_pl1_dm32_nh8_el2_dl1_df32_expand2_dc4_fc3_ebtimeF_dtTrue_Exp_0/true.npy')
y_pred = np.load('/home/lenovo/yinzhou/Time-Series-Library/results/long_term_forecast_custom_timesnet_TimesNet_custom_ftMS_sl256_ll128_pl1_dm32_nh8_el2_dl1_df32_expand2_dc4_fc3_ebtimeF_dtTrue_Exp_0/pred.npy')

# 调整形状：从(11437, 1, 1)展平为一维数组(11437,)
y_true = y_true.reshape(-1)
y_pred = y_pred.reshape(-1)

# 计算指标
r2 = r2_score(y_true, y_pred)
corr, _ = pearsonr(y_true, y_pred)

# 输出结果
print("测试集结果:")
print(f"R²系数: {r2:.4f}")
print(f"皮尔逊相关系数: {corr:.4f}")