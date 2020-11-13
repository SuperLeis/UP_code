'''
    #高风险商户
    machnt = machnt.fillna(0)
    machnt['中高风险金额占比'] = machnt['中风险金额占比'] + machnt['高风险金额占比']
    machnt['风险金额占比'] = machnt['中风险金额占比'] + machnt['高风险金额占比']+machnt['低风险金额占比']

    high_risk_machnt = machnt[machnt['交易笔数']>10]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['贷记卡金额占比']>0.85]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['总金额']>30000]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['笔均金额']>3000]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['大于4800笔数占比']>0.6]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['贷记卡卡均交易金额']>8000]
    #high_risk_machnt = high_risk_machnt[high_risk_machnt['单张贷记卡交易金额占商户当日总交易金额中最大的占比']>0.2]
    high_risk_machnt_1 = high_risk_machnt[high_risk_machnt['中高风险金额占比']>0.6]
    high_risk_machnt_1['商户套现风险分级'] = '高风险1'

    high_risk_machnt = machnt[machnt['交易笔数']>6]
    high_risk_machnt = high_risk_machnt[~high_risk_machnt['mchnt_cd'].isin(high_risk_machnt_1['mchnt_cd'])]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['贷记卡金额占比']>0.85]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['总金额']>25000]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['笔均金额']>3000]
    high_risk_machnt_2 = high_risk_machnt[high_risk_machnt['高风险笔数']>2]
    high_risk_machnt_2['商户套现风险分级'] = '高风险2'

    high_risk_machnt = high_risk_machnt[~high_risk_machnt['mchnt_cd'].isin(high_risk_machnt_1['mchnt_cd'])]
    high_risk_machnt = high_risk_machnt[~high_risk_machnt['mchnt_cd'].isin(high_risk_machnt_2['mchnt_cd'])]
    high_risk_machnt = machnt[machnt['交易笔数']>10]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['贷记卡金额占比']>0.85]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['总金额']>25000]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['笔均金额']>3000]
    high_risk_machnt = high_risk_machnt[high_risk_machnt['贷记卡卡均交易金额']>8000]
    high_risk_machnt_3 = high_risk_machnt[high_risk_machnt['单张贷记卡交易金额占商户当日总交易金额中最大的占比']>0.2]
    high_risk_machnt_3['商户套现风险分级'] = '高风险3'

    high_risk_machnt = pd.concat([high_risk_machnt_1,high_risk_machnt_2,high_risk_machnt_3], axis=0)
    #high_risk_machnt['商户套现风险分级'] = '高风险'

    #中风险商户
    mid_risk_machnt = machnt[machnt['交易笔数']>4]
    mid_risk_machnt = mid_risk_machnt[~mid_risk_machnt['mchnt_cd'].isin(high_risk_machnt['mchnt_cd'])]
    mid_risk_machnt = mid_risk_machnt[mid_risk_machnt['贷记卡金额占比']>0.85]
    mid_risk_machnt = mid_risk_machnt[mid_risk_machnt['笔均金额']>2500]
    mid_risk_machnt_1 = mid_risk_machnt[mid_risk_machnt['中高风险金额占比']>0.35]
    mid_risk_machnt_1['商户套现风险分级'] = '中风险1'

    mid_risk_machnt = machnt[machnt['交易笔数']>5]
    mid_risk_machnt = mid_risk_machnt[~mid_risk_machnt['mchnt_cd'].isin(high_risk_machnt['mchnt_cd'])]
    mid_risk_machnt = mid_risk_machnt[~mid_risk_machnt['mchnt_cd'].isin(mid_risk_machnt_1['mchnt_cd'])]
    mid_risk_machnt = mid_risk_machnt[mid_risk_machnt['笔均金额']>2500]
    mid_risk_machnt = mid_risk_machnt[mid_risk_machnt['贷记卡金额占比']>0.85]
    mid_risk_machnt_2 = mid_risk_machnt[mid_risk_machnt['高风险笔数']>1]
    mid_risk_machnt_2['商户套现风险分级'] = '中风险2'

    mid_risk_machnt = machnt[machnt['交易笔数']>5]
    mid_risk_machnt = mid_risk_machnt[~mid_risk_machnt['mchnt_cd'].isin(high_risk_machnt['mchnt_cd'])]
    mid_risk_machnt = mid_risk_machnt[~mid_risk_machnt['mchnt_cd'].isin(mid_risk_machnt_1['mchnt_cd'])]
    mid_risk_machnt = mid_risk_machnt[~mid_risk_machnt['mchnt_cd'].isin(mid_risk_machnt_2['mchnt_cd'])]
    mid_risk_machnt = mid_risk_machnt[mid_risk_machnt['笔均金额']>2500]
    mid_risk_machnt = mid_risk_machnt[mid_risk_machnt['贷记卡金额占比']>0.85]
    mid_risk_machnt = mid_risk_machnt[mid_risk_machnt['总金额']>20000]
    mid_risk_machnt_3 = mid_risk_machnt[mid_risk_machnt['贷记卡卡均交易金额']>5000]
    mid_risk_machnt_3['商户套现风险分级'] = '中风险3'
    mid_risk_machnt = pd.concat([mid_risk_machnt_1,mid_risk_machnt_2,mid_risk_machnt_3], axis=0)
    #mid_risk_machnt['商户套现风险分级'] = '中风险'

    #低风险商户
    low_risk_machnt = machnt[~machnt['mchnt_cd'].isin(high_risk_machnt['mchnt_cd'])]
    low_risk_machnt = low_risk_machnt[~low_risk_machnt['mchnt_cd'].isin(mid_risk_machnt['mchnt_cd'])]

    non_risk_machnt = low_risk_machnt[low_risk_machnt['交易笔数']==1]
    non_risk_machnt = non_risk_machnt[non_risk_machnt['高风险金额']==0]
    non_risk_machnt_1 = non_risk_machnt[non_risk_machnt['中风险金额']==0]

    low_risk_machnt_raw = low_risk_machnt[~low_risk_machnt['mchnt_cd'].isin(non_risk_machnt_1['mchnt_cd'])]
    low_risk_machnt = low_risk_machnt_raw[low_risk_machnt_raw['总金额']>10000]
    low_risk_machnt = low_risk_machnt[low_risk_machnt['交易笔数']>5]
    low_risk_machnt = low_risk_machnt[low_risk_machnt['贷记卡金额占比']>0.85]

    non_risk_machnt_2 = low_risk_machnt_raw[~low_risk_machnt_raw['mchnt_cd'].isin(low_risk_machnt['mchnt_cd'])]

    low_risk_machnt['商户套现风险分级'] = '低风险'
    non_risk_machnt = pd.concat([non_risk_machnt_1,non_risk_machnt_2], axis=0)
    non_risk_machnt['商户套现风险分级'] = '暂无风险'
'''