import pandas as pd
import os
import asyncio
from js import document, console, window, Object, fileSizeCheck
from pyodide.ffi import create_proxy, to_js
import warnings

warnings.simplefilter(action = 'ignore', category = pd.errors.PerformanceWarning) # Ignores the performance warnings for the data table

def makeDataTable(file):
    squad_rawdata_list = pd.read_html(file, header=0, encoding="utf-8", keep_default_na=False)
    squad_rawdata = squad_rawdata_list[0]
    print("Made Data Table")
    return squad_rawdata

def calcStats(squad_rawdata):
    # Calculate simple speed and workrate scores
    squad_rawdata['Spd'] = ( squad_rawdata['Pac'] + squad_rawdata['Acc'] ) / 2
    squad_rawdata['Work'] = ( squad_rawdata['Wor'] + squad_rawdata['Sta'] ) / 2
    squad_rawdata['SetP'] = ( squad_rawdata['Jum'] + squad_rawdata['Bra'] ) / 2 #Not sure I agree with this for calculating set piece ability
    print("After basics")
    
    # calculates gk score
    squad_rawdata['gk_essential'] = ( 
        squad_rawdata['Agi'] + 
        squad_rawdata['Ref'])
    squad_rawdata['gk_core'] = ( 
        squad_rawdata['1v1'] + 
        squad_rawdata['Ant'] + 
        squad_rawdata['Cmd'] + 
        squad_rawdata['Cnt'] + 
        squad_rawdata['Kic'] + 
        squad_rawdata['Pos'])
    squad_rawdata['gk_secondary'] = ( 
        squad_rawdata['Acc'] +
        squad_rawdata['Aer'] +
        squad_rawdata['Cmp'] + 
        squad_rawdata['Dec'] + 
        squad_rawdata['Fir'] + 
        squad_rawdata['Han'] + 
        squad_rawdata['Pas'] + 
        squad_rawdata['Thr'] + 
        squad_rawdata['Vis'])
    squad_rawdata['gk'] = (((squad_rawdata['gk_essential'] * 5) + (squad_rawdata['gk_core'] * 3) + (squad_rawdata['gk_secondary'] * 1)) / 37 )
    squad_rawdata.gk = squad_rawdata.gk.round(1)
    print("After gk")
    
    # Calculates Sweeper Keeper score
    squad_rawdata['sw_gk_essential']  = ( 
        squad_rawdata['Agi'] + 
        squad_rawdata['Ref'] + 
        squad_rawdata['Ant'])
    squad_rawdata['sw_gk_core'] = (
        squad_rawdata['1v1'] + 
        squad_rawdata['Cmd'] + 
        squad_rawdata['Cnt'] + 
        squad_rawdata['Kic'] + 
        squad_rawdata['Pos'] +
        squad_rawdata['Com'])
    squad_rawdata['sw_gk_secondary'] = ( 
        squad_rawdata['Acc'] +
        squad_rawdata['Aer'] +
        squad_rawdata['Cmp'] + 
        squad_rawdata['Dec'] + 
        squad_rawdata['Fir'] + 
        squad_rawdata['Han'] + 
        squad_rawdata['Pas'] + 
        squad_rawdata['Thr'] + 
        squad_rawdata['Vis'])
    squad_rawdata['sw_gk'] = (((squad_rawdata['sw_gk_essential'] * 5) + (squad_rawdata['sw_gk_core'] * 3) + (squad_rawdata['sw_gk_secondary'] * 1)) / 42 )
    squad_rawdata.sw_gk = squad_rawdata.sw_gk.round(1)
    print("After sw_gk")
    
    # calculates fb score
    squad_rawdata['fb_essential'] = ( 
        squad_rawdata['Wor'] +
        squad_rawdata['Acc'] + 
        squad_rawdata['Pac'] + 
        squad_rawdata['Sta'])
    squad_rawdata['fb_core'] = ( 
        squad_rawdata['Cro'] + 
        squad_rawdata['Dri'] + 
        squad_rawdata['Mar'] + 
        squad_rawdata['OtB'] + 
        squad_rawdata['Tck'] + 
        squad_rawdata['Tea'])
    squad_rawdata['fb_secondary'] = ( 
        squad_rawdata['Agi'] + 
        squad_rawdata['Ant'] + 
        squad_rawdata['Cnt'] + 
        squad_rawdata['Dec'] + 
        squad_rawdata['Fir'] + 
        squad_rawdata['Pas'] + 
        squad_rawdata['Pos'] + 
        squad_rawdata['Tec'])
    squad_rawdata['fb'] = (((squad_rawdata['fb_essential'] * 5) + (squad_rawdata['fb_core'] * 3) + (squad_rawdata['fb_secondary'] * 1)) / 46)
    squad_rawdata.fb = squad_rawdata.fb.round(1)
    print("After Full Back")
    
    # Calculates Wing Back Score
    squad_rawdata['wb_essential'] = ( 
        squad_rawdata['Wor'] +
        squad_rawdata['Acc'] + 
        squad_rawdata['Pac'] + 
        squad_rawdata['Sta'])
    squad_rawdata['wb_core'] = ( 
        squad_rawdata['Cro'] + 
        squad_rawdata['Dri'] + 
        squad_rawdata['Mar'] + 
        squad_rawdata['OtB'] + 
        squad_rawdata['Tck'] + 
        squad_rawdata['Dec'] + 
        squad_rawdata['Pas'] + 
        squad_rawdata['Pos'] + 
        squad_rawdata['Tea'])
    squad_rawdata['wb_secondary'] = ( 
        squad_rawdata['Agi'] + 
        squad_rawdata['Ant'] + 
        squad_rawdata['Cnt'] +  
        squad_rawdata['Fir'] + 
        squad_rawdata['Tec'])
    squad_rawdata['wb'] = (((squad_rawdata['wb_essential'] * 5) + (squad_rawdata['wb_core'] * 3) + (squad_rawdata['wb_secondary'] * 1)) / 52)
    squad_rawdata.wb = squad_rawdata.wb.round(1)
    
    # Add CWB
    
    print("After Wing Back")
    # Calculates Inverted Wing Back Score
    squad_rawdata['iwb_essential'] = ( 
        squad_rawdata['Wor'] +
        squad_rawdata['Acc'] + 
        squad_rawdata['Dec'] + 
        squad_rawdata['Sta'])
    squad_rawdata['iwb_core'] = (  
        squad_rawdata['Mar'] + 
        squad_rawdata['Tck'] + 
        squad_rawdata['Pas'] + 
        squad_rawdata['Pos'] + 
        squad_rawdata['Pac'] + 
        squad_rawdata['Cmp'] + 
        squad_rawdata['Fir'] + 
        squad_rawdata['Tea'])
    squad_rawdata['iwb_secondary'] = ( 
        squad_rawdata['Agi'] + 
        squad_rawdata['Ant'] + 
        squad_rawdata['Cnt'] +  
        squad_rawdata['Dri'] +
        squad_rawdata['Cro'] + 
        squad_rawdata['OtB'] + 
        squad_rawdata['Vis'] + 
        squad_rawdata['Tec'])
    squad_rawdata['iwb'] = (((squad_rawdata['iwb_essential'] * 5) + (squad_rawdata['iwb_core'] * 3) + (squad_rawdata['iwb_secondary'] * 1)) / 52)
    squad_rawdata.iwb = squad_rawdata.iwb.round(1)
    
    
    # calculates cb score
    squad_rawdata['cb_core'] = ( 
        squad_rawdata['Cmp'] + 
        squad_rawdata['Hea'] + 
        squad_rawdata['Jum'] + 
        squad_rawdata['Mar'] + 
        squad_rawdata['Pas'] + 
        squad_rawdata['Pos'] + 
        squad_rawdata['Str'] + 
        squad_rawdata['Tck'] + 
        squad_rawdata['Pac']) / 9
    squad_rawdata['cb_secondary'] = ( 
        squad_rawdata['Agg'] + 
        squad_rawdata['Ant'] + 
        squad_rawdata['Bra'] + 
        squad_rawdata['Cnt'] + 
        squad_rawdata['Dec'] + 
        squad_rawdata['Fir'] + 
        squad_rawdata['Tec'] + 
        squad_rawdata['Vis']) / 8
    squad_rawdata['cb'] = ((squad_rawdata['cb_core'] * 0.75) + (squad_rawdata['cb_secondary'] * 0.25))
    squad_rawdata.cb = squad_rawdata.cb.round(1)
    print("After CB")
    
    # Calculates wide cb
    squad_rawdata['widecb_essential'] = ( 
        squad_rawdata['Mar'] +
        squad_rawdata['Pos'] + 
        squad_rawdata['Tck'] + 
        squad_rawdata['Str'])
    squad_rawdata['widecb_core'] = (  
        squad_rawdata['Jum'] + 
        squad_rawdata['Hea'] + 
        squad_rawdata['Pas'] + 
        squad_rawdata['Cmp'] + 
        squad_rawdata['Pac'])
    squad_rawdata['widecb_secondary'] = ( 
        squad_rawdata['Fir'] + 
        squad_rawdata['Ant'] + 
        squad_rawdata['Cnt'] +  
        squad_rawdata['Dri'] +
        squad_rawdata['Wor'] + 
        squad_rawdata['Dec'] + 
        squad_rawdata['Ant'] + 
        squad_rawdata['Tec'])
    squad_rawdata['widecb'] = (((squad_rawdata['widecb_essential'] * 5) + ( squad_rawdata['widecb_core'] * 3) + (squad_rawdata['widecb_secondary'] * 1)) / 43)
    squad_rawdata.widecb = squad_rawdata.widecb.round(1)
    print("After Wide CB")
    
    # Calculates ball playing Cb
    squad_rawdata['ballcb_essential'] = ( 
        squad_rawdata['Mar'] +
        squad_rawdata['Pos'] + 
        squad_rawdata['Tck'] + 
        squad_rawdata['Str'])
    squad_rawdata['ballcb_core'] = (  
        squad_rawdata['Jum'] + 
        squad_rawdata['Hea'] + 
        squad_rawdata['Pas'] + 
        squad_rawdata['Cmp'] + 
        squad_rawdata['Vis'] +
        squad_rawdata['Pac'])
    squad_rawdata['ballcb_secondary'] = ( 
        squad_rawdata['Fir'] + 
        squad_rawdata['Ant'] + 
        squad_rawdata['Cnt'] +  
        squad_rawdata['Wor'] + 
        squad_rawdata['Dec'] + 
        squad_rawdata['Ant'] + 
        squad_rawdata['Tec'])
    squad_rawdata['ballcb'] = (((squad_rawdata['ballcb_essential'] * 5) + (squad_rawdata['ballcb_core'] * 3) + (squad_rawdata['ballcb_secondary'] * 1)) / 45)
    squad_rawdata.ballcb = squad_rawdata.ballcb.round(1)
    print("After Ball CB")
    
    # Calculates Libero
    squad_rawdata['libero_essential'] = ( 
        squad_rawdata['Mar'] +
        squad_rawdata['Pos'] + 
        squad_rawdata['Tck'] + 
        squad_rawdata['Pas'] + 
        squad_rawdata['Str'])
    squad_rawdata['libero_core'] = (  
        squad_rawdata['Jum'] + 
        squad_rawdata['Hea'] + 
        squad_rawdata['Cmp'] + 
        squad_rawdata['Vis'] +
        squad_rawdata['Tea'] +
        squad_rawdata['Fir'] + 
        squad_rawdata['Dec'] + 
        squad_rawdata['Pac'])
    squad_rawdata['libero_secondary'] = ( 
        squad_rawdata['Ant'] + 
        squad_rawdata['Cnt'] +  
        squad_rawdata['Wor'] + 
        squad_rawdata['Ant'] + 
        squad_rawdata['Sta'] + 
        squad_rawdata['Tec'])
    squad_rawdata['libero'] = (((squad_rawdata['libero_essential'] * 5) + (squad_rawdata['libero_core'] * 3) + (squad_rawdata['libero_secondary'] * 1)) / 55)
    squad_rawdata.libero = squad_rawdata.libero.round(1)
    print("After Libero")
    
    # calculates dm score
    squad_rawdata['dm_essential'] = (
        squad_rawdata['Wor'] +
        squad_rawdata['Tck'])
    squad_rawdata['dm_core'] = (
        squad_rawdata['Sta'] +
        squad_rawdata['Pas'] +
        squad_rawdata['Dec'] +
        squad_rawdata['Ant'] + 
        squad_rawdata['Cnt'] + 
        squad_rawdata['Pos'] + 
        squad_rawdata['Tea'] + 
        squad_rawdata['Cmp'])  
    squad_rawdata['dm_secondary'] = (
        squad_rawdata['Agi'] + 
        squad_rawdata['Bal'] +
        squad_rawdata['Fir'] +
        squad_rawdata['Mar'] +
        squad_rawdata['Agg'] +
        squad_rawdata['Pac'] +
        squad_rawdata['Str'])    
    squad_rawdata['dm'] = (((squad_rawdata['dm_essential'] * 5) + (squad_rawdata['dm_core'] * 3) + (squad_rawdata['dm_secondary'] * 1)) / 41)
    squad_rawdata.dm = squad_rawdata.dm.round(1)
    print("After DM")
    
    # calculates segundo volante on attack score
    squad_rawdata['vol_essential'] = (
        squad_rawdata['Wor'] +
        squad_rawdata['Pac'])
    squad_rawdata['vol_core'] = (
        squad_rawdata['Sta'] +
        squad_rawdata['Pas'] +
        squad_rawdata['Tck'] +
        squad_rawdata['Ant'] + 
        squad_rawdata['Cnt'] + 
        squad_rawdata['Pos'] + 
        squad_rawdata['Tea'])  
    squad_rawdata['vol_secondary'] = (
        squad_rawdata['Bal'] +
        squad_rawdata['Fir'] +
        squad_rawdata['Mar'] +
        squad_rawdata['Agg'] +
        squad_rawdata['Cmp'] +
        squad_rawdata['Dec'] +
        squad_rawdata['Fir'] + 
        squad_rawdata['OtB'] +
        squad_rawdata['Fin'] +
        squad_rawdata['Str'])    
    squad_rawdata['vol'] = (((squad_rawdata['vol_essential'] * 5) + (squad_rawdata['vol_core'] * 3) + (squad_rawdata['vol_secondary'] * 1)) / 41)
    squad_rawdata.vol = squad_rawdata.vol.round(1)
    print("After Vol")
    
    # Calculates DLP
    squad_rawdata['dlp_essential'] = (
        squad_rawdata['Vis'] +
        squad_rawdata['Tea'] +
        squad_rawdata['Pas'])
    squad_rawdata['dlp_core'] = (
        squad_rawdata['Tck'] +
        squad_rawdata['Tec'] +
        squad_rawdata['Cmp'] +
        squad_rawdata['Dec'] +
        squad_rawdata['Ant'] + 
        squad_rawdata['Pos'])  
    squad_rawdata['dlp_secondary'] = (
        squad_rawdata['Bal'] +
        squad_rawdata['Fir'] +
        squad_rawdata['Mar'] +
        squad_rawdata['Fir'] + 
        squad_rawdata['OtB'])    
    squad_rawdata['dlp'] = (((squad_rawdata['dlp_essential'] * 5) + (squad_rawdata['dlp_core'] * 3) + (squad_rawdata['dlp_secondary'] * 1)) / 38)
    squad_rawdata.dlp = squad_rawdata.dlp.round(1)
    print("After DLP")
    
    # Calculate Regista
    squad_rawdata['reg_essential'] = (
        squad_rawdata['Vis'] +
        squad_rawdata['Tea'] +
        squad_rawdata['Cmp'] +
        squad_rawdata['Pas'])
    squad_rawdata['reg_core'] = (
        squad_rawdata['Tck'] +
        squad_rawdata['Tec'] +
        squad_rawdata['Dec'] +
        squad_rawdata['Ant'] + 
        squad_rawdata['OtB'])
    squad_rawdata['reg_secondary'] = (
        squad_rawdata['Bal'] +
        squad_rawdata['Fir'] +
        squad_rawdata['Mar'] +
        squad_rawdata['Fir'] + 
        squad_rawdata['Pos'] + 
        squad_rawdata['Fla'])     
    squad_rawdata['reg'] = (((squad_rawdata['reg_essential'] * 5) + (squad_rawdata['reg_core'] * 3) + (squad_rawdata['reg_secondary'] * 1)) / 41)
    squad_rawdata.reg = squad_rawdata.reg.round(1)
    print("After Regista")
    
    # Calculates Half back
    squad_rawdata['hb_essential'] = (
        squad_rawdata['Pos'] +
        squad_rawdata['Dec'] +
        squad_rawdata['Mar'] +
        squad_rawdata['Tck'])
    squad_rawdata['hb_core'] = (
        squad_rawdata['Sta'] +
        squad_rawdata['Ant'] + 
        squad_rawdata['Cnt'] + 
        squad_rawdata['Cmp'] +
        squad_rawdata['Tea'])  
    squad_rawdata['hb_secondary'] = (
        squad_rawdata['Fir'] +
        squad_rawdata['Agg'] +
        squad_rawdata['Pas'] +
        squad_rawdata['Fir'] + 
        squad_rawdata['Wor'] +
        squad_rawdata['Sta'] +
        squad_rawdata['Str'])    
    squad_rawdata['hb'] = (((squad_rawdata['hb_essential'] * 5) + (squad_rawdata['hb_core'] * 3) + (squad_rawdata['hb_secondary'] * 1)) / 42)
    squad_rawdata.hb = squad_rawdata.hb.round(1)
    print("After HB")
    
    # calculates box2box score, also does enough for CM
    squad_rawdata['box2_essential'] = (
        squad_rawdata['Pas'] +
        squad_rawdata['Wor'] +
        squad_rawdata['Sta'])
    squad_rawdata['box2_core'] = (
        squad_rawdata['Tck'] +
        squad_rawdata['OtB'] + 
        squad_rawdata['Vis'] + 
        squad_rawdata['Str'] +
        squad_rawdata['Dec'] +
        squad_rawdata['Pos'] +
        squad_rawdata['Pac'] +
        squad_rawdata['Tea'])  
    squad_rawdata['box2_secondary'] = (
        squad_rawdata['Fir'] +
        squad_rawdata['Agg'] +
        squad_rawdata['Tec'] +
        squad_rawdata['Lon'] + 
        squad_rawdata['Dri'] +
        squad_rawdata['Ant'] +
        squad_rawdata['Acc'] +
        squad_rawdata['Bal'] +
        squad_rawdata['Fin'])  
    squad_rawdata['box2'] = ((( squad_rawdata['box2_essential'] * 5) + ( squad_rawdata['box2_core'] * 3) + (squad_rawdata['box2_secondary'] * 1)) / 48)
    squad_rawdata.box2 = squad_rawdata.box2.round(1)
    print("After B2B")
    
    #Add Carrilero
    
    # Add Mezzala
    squad_rawdata['mez_essential'] = (
        squad_rawdata['Pas'] +
        squad_rawdata['Wor'] +
        squad_rawdata['Acc'] +
        squad_rawdata['OtB'])
    squad_rawdata['mez_core'] = (
        squad_rawdata['Vis'] + 
        squad_rawdata['Sta'] +
        squad_rawdata['Dec'] +
        squad_rawdata['Tec'] +
        squad_rawdata['Pac'])  
    squad_rawdata['mez_secondary'] = (
        squad_rawdata['Fir'] +
        squad_rawdata['Tck'] +
        squad_rawdata['Dri'] +
        squad_rawdata['Lon'] + 
        squad_rawdata['Ant'] +
        squad_rawdata['Cmp'] +
        squad_rawdata['Bal'] +
        squad_rawdata['Tea'] +
        squad_rawdata['Fin'])  
    squad_rawdata['mez'] = ((( squad_rawdata['mez_essential'] * 5) + ( squad_rawdata['mez_core'] * 3) + (squad_rawdata['mez_secondary'] * 1)) / 44)
    squad_rawdata.mez = squad_rawdata.mez.round(1)
    print("After Mez")
    
    # Add AP
    squad_rawdata['ap_essential'] = (
        squad_rawdata['Pas'] +
        squad_rawdata['Vis'] +
        squad_rawdata['Dec'] +
        squad_rawdata['OtB'])
    squad_rawdata['ap_core'] = (
        squad_rawdata['Tea'] + 
        squad_rawdata['Cmp'] +
        squad_rawdata['Tec'] +
        squad_rawdata['Fir'] +
        squad_rawdata['Agi'])  
    squad_rawdata['ap_secondary'] = (
        squad_rawdata['Fla'] +
        squad_rawdata['Dri'] +
        squad_rawdata['Ant'] +
        squad_rawdata['Acc'])  
    squad_rawdata['ap'] = ((( squad_rawdata['ap_essential'] * 5) + ( squad_rawdata['ap_core'] * 3) + (squad_rawdata['ap_secondary'] * 1)) / 39)
    squad_rawdata.ap = squad_rawdata.ap.round(1)
    print("After AP")
    
    # Calculate BWM
    squad_rawdata['bwm_essential'] = (
        squad_rawdata['Sta'] +
        squad_rawdata['Wor'] +
        squad_rawdata['Tck'] +
        squad_rawdata['Tea'])
    squad_rawdata['bwm_core'] = (
        squad_rawdata['Agg'] + 
        squad_rawdata['Ant'] +
        squad_rawdata['Pos'] +
        squad_rawdata['Str'] +
        squad_rawdata['Pac'])  
    squad_rawdata['bwm_secondary'] = (
        squad_rawdata['Dec'] +
        squad_rawdata['Cmp'] +
        squad_rawdata['Agi'] +
        squad_rawdata['Mar'] +
        squad_rawdata['Pas'] +
        squad_rawdata['Cnt'])  
    squad_rawdata['bwm'] = ((( squad_rawdata['bwm_essential'] * 5) + ( squad_rawdata['bwm_core'] * 3) + (squad_rawdata['bwm_secondary'] * 1)) / 41)
    squad_rawdata.bwm = squad_rawdata.bwm.round(1)
    print("After BWM")
    
    # Calculate Roaming Playmaker
    squad_rawdata['rp_essential'] = (
        squad_rawdata['Sta'] +
        squad_rawdata['Wor'] +
        squad_rawdata['Vis'] +
        squad_rawdata['Pas'] +
        squad_rawdata['Tea'])
    squad_rawdata['rp_core'] = (
        squad_rawdata['OtB'] + 
        squad_rawdata['Ant'] +
        squad_rawdata['Cmp'] +
        squad_rawdata['Acc'] +
        squad_rawdata['Pac'])  
    squad_rawdata['rp_secondary'] = (
        squad_rawdata['Dec'] +
        squad_rawdata['Pos'] +
        squad_rawdata['Agi'] +
        squad_rawdata['Fir'] +
        squad_rawdata['Tec'] +
        squad_rawdata['Dri'] +
        squad_rawdata['Bal'] +
        squad_rawdata['Cnt'])  
    squad_rawdata['rp'] = ((( squad_rawdata['rp_essential'] * 5) + ( squad_rawdata['rp_core'] * 3) + (squad_rawdata['rp_secondary'] * 1)) / 48)
    squad_rawdata.rp = squad_rawdata.rp.round(1)
    print("After RP")
    
    # calculates winger score
    squad_rawdata['w_core'] = ( 
        squad_rawdata['Acc'] + 
        squad_rawdata['Cro'] + 
        squad_rawdata['Dri'] + 
        squad_rawdata['OtB'] + 
        squad_rawdata['Pac'] + 
        squad_rawdata['Tec']) / 6
    squad_rawdata['w_secondary'] = ( 
        squad_rawdata['Agi'] + 
        squad_rawdata['Fir'] + 
        squad_rawdata['Pas'] + 
        squad_rawdata['Sta'] +
        squad_rawdata['Bal'] + 
        squad_rawdata['Wor']) / 6
    squad_rawdata['w'] = (( squad_rawdata['w_core'] * 0.75) + (squad_rawdata['w_secondary'] * 0.25))
    squad_rawdata.w = squad_rawdata.w.round(1)
    print("After Winger")
    
    # calculates inverted winger score 
    squad_rawdata['invw_essential'] = (
        squad_rawdata['Pac'] +
        squad_rawdata['Acc'] +
        squad_rawdata['Wor'] +
        squad_rawdata['Pas'])
    squad_rawdata['invw_core'] = (
        squad_rawdata['OtB'] + 
        squad_rawdata['Pas'] +
        squad_rawdata['Dri'] +
        squad_rawdata['Tec'] +
        squad_rawdata['Agi'])  
    squad_rawdata['invw_secondary'] = (
        squad_rawdata['Dec'] +
        squad_rawdata['Cmp'] +
        squad_rawdata['Ant'] +
        squad_rawdata['Fir'] +
        squad_rawdata['Cro'] +
        squad_rawdata['Lon'] +
        squad_rawdata['Vis'] +
        squad_rawdata['Sta'])  
    squad_rawdata['invw'] = ((( squad_rawdata['invw_essential'] * 5) + ( squad_rawdata['invw_core'] * 3) + (squad_rawdata['invw_secondary'] * 1)) / 43)
    squad_rawdata.invw = squad_rawdata.invw.round(1)
    print("After inv W")
    
    # Calculate Wide TF
    squad_rawdata['wtf_essential'] = (
        squad_rawdata['Str'] +
        squad_rawdata['Jum'] +
        squad_rawdata['Hea'] +
        squad_rawdata['OtB'])
    squad_rawdata['wtf_core'] = (
        squad_rawdata['Fir'] + 
        squad_rawdata['Bra'] +
        squad_rawdata['Tea'] +
        squad_rawdata['Wor'] +
        squad_rawdata['Sta'])  
    squad_rawdata['wtf_secondary'] = (
        squad_rawdata['Cro'] +
        squad_rawdata['Bal'] +
        squad_rawdata['Ant'])  
    squad_rawdata['wtf'] = ((( squad_rawdata['wtf_essential'] * 5) + ( squad_rawdata['wtf_core'] * 3) + (squad_rawdata['wtf_secondary'] * 1)) / 38)
    squad_rawdata.wtf = squad_rawdata.wtf.round(1)
    print("After WTF")
    
    # Calculate IF
    squad_rawdata['insf_essential'] = (
        squad_rawdata['Dri'] +
        squad_rawdata['Acc'] +
        squad_rawdata['Fin'] +
        squad_rawdata['Agi'] +
        squad_rawdata['Fir'])
    squad_rawdata['insf_core'] = (
        squad_rawdata['OtB'] + 
        squad_rawdata['Pas'] +
        squad_rawdata['Cmp'] +
        squad_rawdata['Tec'] +
        squad_rawdata['Pac'] +
        squad_rawdata['Bal'])  
    squad_rawdata['insf_secondary'] = (
        squad_rawdata['Sta'] +
        squad_rawdata['Ant'] +
        squad_rawdata['Fla'] +
        squad_rawdata['Lon'] +
        squad_rawdata['Vis'] +
        squad_rawdata['Dec'] +
        squad_rawdata['Wor'])  
    squad_rawdata['insf'] = ((( squad_rawdata['insf_essential'] * 5) + ( squad_rawdata['insf_core'] * 3) + (squad_rawdata['insf_secondary'] * 1)) / 50)
    squad_rawdata.insf = squad_rawdata.insf.round(1)
    print("After IF")
    
    # Calculate Ramdeuter 
    squad_rawdata['ram_essential'] = (
        squad_rawdata['OtB'] +
        squad_rawdata['Dec'] +
        squad_rawdata['Fin'] +
        squad_rawdata['Cmp'] +
        squad_rawdata['Cnt'])
    squad_rawdata['ram_core'] = (
        squad_rawdata['Ant'] + 
        squad_rawdata['Pas'] +
        squad_rawdata['Tec'] +
        squad_rawdata['Acc'] +
        squad_rawdata['Bal'])  
    squad_rawdata['ram_secondary'] = (
        squad_rawdata['Sta'] +
        squad_rawdata['Vis'] +
        squad_rawdata['Wor'])  
    squad_rawdata['ram'] = (((squad_rawdata['ram_essential'] * 5) + (squad_rawdata['ram_core'] * 3) + (squad_rawdata['ram_secondary'] * 1)) / 43)
    squad_rawdata.ram = squad_rawdata.ram.round(1)
    print("After Ramdeuter")
    
    # Calculate Trequartista
    squad_rawdata['trq_essential'] = (
        squad_rawdata['OtB'] +
        squad_rawdata['Dec'] +
        squad_rawdata['Fin'] +
        squad_rawdata['Cmp'] +
        squad_rawdata['Dri'])
    squad_rawdata['trq_core'] = (
        squad_rawdata['Pas'] +
        squad_rawdata['Fir'] + 
        squad_rawdata['Tec'] +
        squad_rawdata['Acc'] +
        squad_rawdata['Agi'] +
        squad_rawdata['Vis'] +
        squad_rawdata['Bal'])  
    squad_rawdata['trq_secondary'] = (
        squad_rawdata['Fla'] +
        squad_rawdata['Ant'] + 
        squad_rawdata['Lon'])  
    squad_rawdata['trq'] = (((squad_rawdata['trq_essential'] * 5) + (squad_rawdata['trq_core'] * 3) + (squad_rawdata['trq_secondary'] * 1)) / 49)
    squad_rawdata.trq = squad_rawdata.trq.round(1)
    print("After Treq")
    
    # calculates amc score
    squad_rawdata['amc_essential'] = (
        squad_rawdata['Vis'] +
        squad_rawdata['Dec'] +
        squad_rawdata['OtB'] +
        squad_rawdata['Pas'])
    squad_rawdata['amc_core'] = (
        squad_rawdata['Cmp'] +
        squad_rawdata['Fir'] + 
        squad_rawdata['Tec'] +
        squad_rawdata['Dri'] +
        squad_rawdata['Ant'])  
    squad_rawdata['amc_secondary'] = (
        squad_rawdata['Fla'] +
        squad_rawdata['Cmp'] + 
        squad_rawdata['Agi'] +
        squad_rawdata['Fin'] + 
        squad_rawdata['Lon'])  
    squad_rawdata['amc'] = (((squad_rawdata['amc_essential'] * 5) + (squad_rawdata['amc_core'] * 3) + (squad_rawdata['amc_secondary'] * 1)) / 40)
    squad_rawdata.amc = squad_rawdata.amc.round(1)
    print("After AMC")
    
    # Calculate Shadow ST
    squad_rawdata['shadowst_essential'] = (
        squad_rawdata['Dri'] +
        squad_rawdata['Fin'] +
        squad_rawdata['Fir'] +
        squad_rawdata['OtB'])
    squad_rawdata['shadowst_core'] = (
        squad_rawdata['Cmp'] +
        squad_rawdata['Ant'] + 
        squad_rawdata['Acc'] +
        squad_rawdata['Pac'] +
        squad_rawdata['Agi'])  
    squad_rawdata['shadowst_secondary'] = (
        squad_rawdata['Wor'] +
        squad_rawdata['Pas'] + 
        squad_rawdata['Tec'] +
        squad_rawdata['Bal'] + 
        squad_rawdata['Dec'] +
        squad_rawdata['Cnt'] +  
        squad_rawdata['Sta'])  
    squad_rawdata['shadowst'] = (((squad_rawdata['shadowst_essential'] * 5) + (squad_rawdata['shadowst_core'] * 3) + (squad_rawdata['shadowst_secondary'] * 1)) / 42)
    squad_rawdata.shadowst = squad_rawdata.shadowst.round(1)
    print("After SST")
    
    # Calculate Enganche
    squad_rawdata['eng_essential'] = (
        squad_rawdata['Pas'] +
        squad_rawdata['Vis'] +
        squad_rawdata['Fir'] +
        squad_rawdata['Dec'])
    squad_rawdata['eng_core'] = (
        squad_rawdata['Cmp'] +
        squad_rawdata['Ant'] + 
        squad_rawdata['Cmp'])  
    squad_rawdata['eng_secondary'] = (
        squad_rawdata['Tea'] +
        squad_rawdata['Dri'] + 
        squad_rawdata['Tec'] +
        squad_rawdata['Agi'] + 
        squad_rawdata['Fla'] +
        squad_rawdata['OtB'] +  
        squad_rawdata['Lon'])  
    squad_rawdata['eng'] = (((squad_rawdata['eng_essential'] * 5) + (squad_rawdata['eng_core'] * 3) + (squad_rawdata['eng_secondary'] * 1)) / 36)
    squad_rawdata.eng = squad_rawdata.eng.round(1)
    print("After Enganche")
    
    # calculates striker score
    squad_rawdata['str_core'] = ( 
        squad_rawdata['Cmp'] + 
        squad_rawdata['Fin'] + 
        squad_rawdata['OtB'] + 
        squad_rawdata['Pac']) / 4
    squad_rawdata['str_secondary'] = ( 
        squad_rawdata['Acc'] + 
        squad_rawdata['Agi'] + 
        squad_rawdata['Ant'] + 
        squad_rawdata['Bal'] + 
        squad_rawdata['Dec'] + 
        squad_rawdata['Dri'] + 
        squad_rawdata['Fir'] + 
        squad_rawdata['Pas'] + 
        squad_rawdata['Sta'] + 
        squad_rawdata['Tec'] + 
        squad_rawdata['Wor']) / 11
    squad_rawdata['str'] = (( squad_rawdata['str_core'] * 0.5) + (squad_rawdata['str_secondary'] * 0.5))
    squad_rawdata.str = squad_rawdata.str.round(1)
    print("After Str")
    
    # Calculate AF
    squad_rawdata['af_essential'] = (
        squad_rawdata['Dri'] +
        squad_rawdata['Fin'] +
        squad_rawdata['Fir'] +
        squad_rawdata['Cmp'])
    squad_rawdata['af_core'] = (
        squad_rawdata['Acc'] +
        squad_rawdata['Tec'] + 
        squad_rawdata['OtB'])  
    squad_rawdata['af_secondary'] = (
        squad_rawdata['Wor'] +
        squad_rawdata['Agi'] + 
        squad_rawdata['Bal'] +
        squad_rawdata['Pac'] + 
        squad_rawdata['Sta'] +
        squad_rawdata['Pas'] +
        squad_rawdata['Ant'] +  
        squad_rawdata['Dec'])  
    squad_rawdata['af'] = (((squad_rawdata['af_essential'] * 5) + (squad_rawdata['af_core'] * 3) + (squad_rawdata['af_secondary'] * 1)) / 37)
    squad_rawdata.af = squad_rawdata.af.round(1)
    print("After AF")
    
    # Calculate PF
    squad_rawdata['pf_essential'] = (
        squad_rawdata['Wor'] +
        squad_rawdata['Tea'] +
        squad_rawdata['Ant'] +
        squad_rawdata['Acc'] +
        squad_rawdata['Pac'])
    squad_rawdata['pf_core'] = (
        squad_rawdata['Agg'] +
        squad_rawdata['Bra'] +
        squad_rawdata['Fin'] + 
        squad_rawdata['OtB'])  
    squad_rawdata['pf_secondary'] = (
        squad_rawdata['Agi'] + 
        squad_rawdata['Bal'] +
        squad_rawdata['Pac'] + 
        squad_rawdata['Sta'] +
        squad_rawdata['Str'] +
        squad_rawdata['Fir'] +  
        squad_rawdata['Dec'])  
    squad_rawdata['pf'] = (((squad_rawdata['pf_essential'] * 5) + (squad_rawdata['pf_core'] * 3) + (squad_rawdata['pf_secondary'] * 1)) / 44)
    squad_rawdata.pf = squad_rawdata.pf.round(1)
    print("After PF")
    
    # Calculate Poacher
    squad_rawdata['poach_essential'] = (
        squad_rawdata['OtB'] +
        squad_rawdata['Ant'] +
        squad_rawdata['Fin'] +
        squad_rawdata['Cmp'])
    squad_rawdata['poach_core'] = (
        squad_rawdata['Acc'] +
        squad_rawdata['Pac'] + 
        squad_rawdata['Dec'])  
    squad_rawdata['poach_secondary'] = (
        squad_rawdata['Fir'] +
        squad_rawdata['Hea'] + 
        squad_rawdata['Tec'])  
    squad_rawdata['poach'] = (((squad_rawdata['poach_essential'] * 5) + (squad_rawdata['poach_core'] * 3) + (squad_rawdata['poach_secondary'] * 1)) / 32)
    squad_rawdata.poach = squad_rawdata.poach.round(1)
    print("After Poach")
    
    # Calculate Complete ST
    squad_rawdata['completest_essential'] = (
        squad_rawdata['Dri'] +
        squad_rawdata['Fin'] +
        squad_rawdata['Fir'] +
        squad_rawdata['OtB'] +
        squad_rawdata['Cmp'])
    squad_rawdata['completest_core'] = (
        squad_rawdata['Acc'] +
        squad_rawdata['Agi'] + 
        squad_rawdata['Ant'] +
        squad_rawdata['Hea'] + 
        squad_rawdata['Tec'] +
        squad_rawdata['Pac'] +   
        squad_rawdata['Str'])  
    squad_rawdata['completest_secondary'] = (
        squad_rawdata['Bal'] +
        squad_rawdata['Jum'] + 
        squad_rawdata['Sta'] +
        squad_rawdata['Lon'] + 
        squad_rawdata['Pas'] +
        squad_rawdata['Vis'] +
        squad_rawdata['Tea'] +  
        squad_rawdata['Wor'])  
    squad_rawdata['completest'] = (((squad_rawdata['completest_essential'] * 5) + (squad_rawdata['completest_core'] * 3) + (squad_rawdata['completest_secondary'] * 1)) / 54)
    squad_rawdata.completest = squad_rawdata.completest.round(1)
    print("After Complete ST")
    
    # Calculate DLF
    squad_rawdata['dlf_essential'] = (
        squad_rawdata['Fir'] +
        squad_rawdata['Pas'] +
        squad_rawdata['Dec'] +
        squad_rawdata['OtB'] +
        squad_rawdata['Tea'])
    squad_rawdata['dlf_core'] = (
        squad_rawdata['Ant'] + 
        squad_rawdata['Dri'] +
        squad_rawdata['Fin'] + 
        squad_rawdata['Tec'] +   
        squad_rawdata['Cmp'])  
    squad_rawdata['dlf_secondary'] = (
        squad_rawdata['Bal'] +
        squad_rawdata['Fla'] + 
        squad_rawdata['Str'] +
        squad_rawdata['Vis'])  
    squad_rawdata['dlf'] = (((squad_rawdata['dlf_essential'] * 5) + (squad_rawdata['dlf_core'] * 3) + (squad_rawdata['dlf_secondary'] * 1)) / 44)
    squad_rawdata.dlf = squad_rawdata.dlf.round(1)
    print("After DLF")
    
    # Calculate TM
    squad_rawdata['tf_essential'] = (
        squad_rawdata['Str'] +
        squad_rawdata['Jum'] +
        squad_rawdata['Hea'] +
        squad_rawdata['Fin'])
    squad_rawdata['tf_core'] = (
        squad_rawdata['Cmp'] +
        squad_rawdata['Dec'] +
        squad_rawdata['Bra'] +
        squad_rawdata['Fir'])  
    squad_rawdata['tf_secondary'] = (
        squad_rawdata['Bal'] +
        squad_rawdata['Tea'] + 
        squad_rawdata['Agg'] +
        squad_rawdata['Pas'])  
    squad_rawdata['tf'] = (((squad_rawdata['tf_essential'] * 5) + (squad_rawdata['tf_core'] * 3) + (squad_rawdata['tf_secondary'] * 1)) / 36)
    squad_rawdata.tf = squad_rawdata.tf.round(1)
    print("After TM")
    
    # Calculate False 9
    squad_rawdata['f9_essential'] = (
        squad_rawdata['Fir'] +
        squad_rawdata['Pas'] +
        squad_rawdata['Dec'] +
        squad_rawdata['OtB'] +
        squad_rawdata['Tea'])
    squad_rawdata['f9_core'] = (
        squad_rawdata['Tea'] +
        squad_rawdata['Ant'] + 
        squad_rawdata['Dri'] +
        squad_rawdata['Fin'] + 
        squad_rawdata['Tec'] +   
        squad_rawdata['Cmp'])  
    squad_rawdata['f9_secondary'] = (
        squad_rawdata['Bal'] +
        squad_rawdata['Fla'] + 
        squad_rawdata['Str'] +
        squad_rawdata['Vis'])  
    squad_rawdata['f9'] = (((squad_rawdata['f9_essential'] * 5) + (squad_rawdata['f9_core'] * 3) + (squad_rawdata['f9_secondary'] * 1)) / 47)
    squad_rawdata.f9 = squad_rawdata.f9.round(1)
    print("After F9")
    
    #TODO: Give ability to chose roles and positions
    #TODO: Add ability to change weightings
    
    # builds squad dataframe using only columns that will be exported to HTML
    squad = squad_rawdata[
        [
        'Inf',
        'Name',
        'Age',
        'Club',
        'Transfer Value',
        'Wage',
        'Nat',
        'Position',
        'Personality',
        'Media Handling',
        'Left Foot',
        'Right Foot',
        'Spd',
        'Jum',
        'Str',
        'Work',
        'Height',
        'gk',
        'sw_gk',
        'fb',
        'wb',
        'iwb',
        'cb',
        'ballcb',
        'widecb',
        'libero',
        'dm',
        'vol',
        'dlp',
        'reg',
        'hb',
        'box2',
        'mez',
        'ap',
        'bwm',
        'rp',
        'w',
        'invw',
        'wtf',
        'insf',
        'ram',
        'trq',
        'amc',
        'shadowst',
        'eng',
        'str',
        'af',
        'pf',
        'poach',
        'completest',
        'dlf',
        'tf',
        'f9'
        ]
    ]
    
    return squad

# taken from here: https://www.thepythoncode.com/article/convert-pandas-dataframe-to-html-table-python
# creates a function to make a sortable html export
def generateHtml(dataframe: pd.DataFrame):
    # get the table HTML from the dataframe
    print("Generating HTML")
    table_html = dataframe.to_html(table_id="table", index=False)
    # construct the complete HTML with jQuery Data tables
    # You can disable paging or enable y scrolling on lines 20 and 21 respectively
    html = f"""
    <html>
    <header>
        <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
    </header>
    <body>
    {table_html}
    <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
    <script>
        $(document).ready( function () {{
            $('#table').DataTable({{
                paging: false,
                order: [[12, 'desc']],
                // scrollY: 400,
            }});
        }});
    </script>
    </body>
    </html>
    """
    # return the html
    return html

async def process_file(event):
    
    # Checks file size using function in js file. If file is too big it stops the execution
    sizeCheck = fileSizeCheck(event.target.files)
    if sizeCheck == False:
        return
    
    #Makes the uploaded file a python object
    fileList = event.target.files.to_py()

    for f in fileList:
        data = await f.text()
        squadRawData = makeDataTable(data)
        # Maybe add a check to see if all necessary attrs exist
        squadData = calcStats(squadRawData)
        weightedData = generateHtml(squadData)
        try:
            # Perform the actual file system save 
            options = {
                "startIn": "downloads",
                "suggestedName": "output.html",
                "types": {
                 "accept": { "text/html": [".html"] }   
                }
            }
            fileHandle = await window.showSaveFilePicker(Object.fromEntries(to_js(options)))
            file = await fileHandle.createWritable()
            await file.write(weightedData)
            await file.close()
        except Exception as e:
            console.log('Exception: ' + str(e))
            return

def main():
    fileEvent = create_proxy(process_file)
    document.getElementById("fileInput").addEventListener("change", fileEvent, False)

main()