import uuid
from datetime import datetime
import pandas as pd
import streamlit as st
from database import init, all_alerts, add, set_status

st.set_page_config(page_title='ResQMesh | Command Center',page_icon='🚨',layout='wide')
init()
st.markdown('''<style>
.stApp {background:#08111f;color:#eaf0fa}
.block-container{padding-top:1.6rem;max-width:1450px}
div[data-testid="stMetric"]{background:#14243a;border:1px solid #2a405a;border-radius:16px;padding:18px}
div[data-testid="stMetricValue"]{color:#f8fbff}
[data-testid="stSidebar"]{background:#0d1a2d}
</style>''',unsafe_allow_html=True)

with st.sidebar:
    st.markdown('## ◈ RESQMESH')
    st.caption('OFFLINE RESPONSE NETWORK')
    st.success('Dashboard running locally')
    st.info('Radio link status is not verified here. A gateway event appears when the USB reader saves it.')
    st.markdown('### Test without hardware')
    if st.button('＋ Generate demo SOS',use_container_width=True):
        add('DEMO-'+uuid.uuid4().hex[:10],'NODE_DEMO','SOS',1,'DEMO_LOCATION',-68,8.2,source='Demo')
        st.rerun()
    if st.button('＋ Generate demo Medical',use_container_width=True):
        add('DEMO-'+uuid.uuid4().hex[:10],'NODE_DEMO','MEDICAL',1,'DEMO_LOCATION',-74,6.5,source='Demo')
        st.rerun()
    st.caption('Demo alerts are clearly marked and are not real LoRa transmissions.')

st.markdown('### 🚨 RESQMESH  /  EMERGENCY COMMAND CENTER')
st.caption('Local operations dashboard • Automatic refresh every 2 seconds • No cloud required')

@st.fragment(run_every='2s')
def live():
    rows=all_alerts()
    total=len(rows)
    active=sum(r['status']!='Resolved' for r in rows)
    critical=sum(r['priority']==1 and r['status']!='Resolved' for r in rows)
    resolved=sum(r['status']=='Resolved' for r in rows)
    a,b,c,d=st.columns(4)
    a.metric('TOTAL ALERTS',total)
    b.metric('🔴 CRITICAL OPEN',critical)
    c.metric('ACTIVE CASES',active)
    d.metric('✓ RESOLVED',resolved)
    st.markdown('---')
    left,right=st.columns([1.8,1])
    with left:
        st.subheader('Live incident feed')
        if not rows:
            st.info('Waiting for emergency signals. To preview the dashboard, use a demo button in the sidebar.')
        else:
            types=['All']+sorted({r['emergency_type'] for r in rows})
            statuses=['All','Pending','In Progress','Resolved']
            x,y=st.columns(2)
            selected_type=x.selectbox('Emergency type',types,key='type_filter')
            selected_status=y.selectbox('Status',statuses,key='status_filter')
            filtered=[r for r in rows if (selected_type=='All' or r['emergency_type']==selected_type) and (selected_status=='All' or r['status']==selected_status)]
            if filtered:
                df=pd.DataFrame(filtered)
                df['severity']=df['priority'].map({1:'🔴 Critical',2:'🟠 High',3:'🟡 Medium'})
                df['received_at']=df['received_at'].str.replace('T',' ',regex=False).str.slice(0,19)+' UTC'
                st.dataframe(df[['received_at','emergency_type','severity','node_id','location','status','rssi','snr','source']].rename(columns={'received_at':'Received','emergency_type':'Emergency','severity':'Priority','node_id':'Node','location':'Location','status':'Status','rssi':'RSSI (dBm)','snr':'SNR (dB)','source':'Source'}),hide_index=True,use_container_width=True)
            else:
                st.info('No incidents match the selected filters.')
    with right:
        st.subheader('Emergency breakdown')
        if rows:
            counts=pd.Series([r['emergency_type'] for r in rows]).value_counts()
            st.bar_chart(counts, horizontal=True)
        else:
            st.caption('No data yet')
        st.markdown('**Network path**')
        st.code('TRANSMITTER → LoRa → GATEWAY → USB → DASHBOARD',language=None)
        st.caption('Locations are manually assigned IDs, not GPS positions.')
    st.markdown('---')
    st.subheader('Incident management')
    open_rows=[r for r in rows if r['status']!='Resolved']
    if not open_rows:
        st.success('No open incidents.')
    for r in open_rows[:100]:
        badge={1:'🔴',2:'🟠',3:'🟡'}.get(r['priority'],'⚪')
        with st.expander(f"{badge} {r['emergency_type']}  ·  {r['node_id']}  ·  {r['location']}  ·  {r['status']}"):
            st.caption(f"Packet: {r['packet_id']}  |  Source: {r['source']}  |  Received: {r['received_at']} UTC")
            st.write(f"Signal: RSSI {r['rssi']} dBm  ·  SNR {r['snr']} dB")
            options=['Pending','In Progress','Resolved']
            with st.form('form_'+r['packet_id']):
                value=st.selectbox('Update incident status',options,index=options.index(r['status']))
                if st.form_submit_button('Save status'):
                    set_status(r['packet_id'],value)
                    st.rerun()
    if rows:
        st.download_button('↓ Export incident history (CSV)',pd.DataFrame(rows).to_csv(index=False).encode('utf-8'),'resqmesh_incidents.csv','text/csv')

live()
st.caption('Prototype only — dashboard receipt or gateway ACK does not imply dispatch or rescue confirmation.')
