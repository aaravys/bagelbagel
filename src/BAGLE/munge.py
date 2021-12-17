import numpy as np
import pylab as plt
from src.BAGLE import model, model_fitter
import dynesty
from dynesty import utils as dyutil
from dynesty import plotting as dyplot
from astropy.table import Table
from astropy.time import Time
from astropy import units 
from astropy.coordinates import SkyCoord
from astropy import time as atime, coordinates as coord, units as u
from multiprocessing import Pool, cpu_count
import time
import pickle
import pdb
import os

ra = {'mb09260' :  '17:58:28.561',
      'mb10364' :  '17:57:05.401',
      'ob110037' : '17:55:55.83',
      'ob110310' : '17:51:25.39',
      'ob110462' : '17:51:40.19',
      'ob110462_corr' : '17:51:40.19',
      'ob120169' : '17:49:51.38',
      'ob140613' : '17:53:57.68', 
      'ob150029' : '17:59:46.60', 
      'ob150211' : '17:29:26.18',
      'ob170302' : '17:41:35.93',
      'ob170328' : '17:54:09.56',
      'ob170019' : '17:52:18.74',
      'ob170095' : '17:51:27.94',
      'ob190017' : '17:59:03.52',
      'ob191000' : '17:47:01.67',
      'ob191080' : '18:10:04.47',
      'ob190241' : '17:54:10.76',
      'kb200101' : '17:45:11.03',
      'kb200122' : '17:40:27.69',
      'kb200122_short' : '17:40:27.69',
      'ob040361' : '17:46:35.41',
      'ob060095' : '17:57:23.14',
      'ob020061' : '17:35:55.97',
      'mb19284'  : '18:05:55.084',}

dec = {'mb09260' :  '-26:50:20.88',
       'mb10364' :  '-34:27:05.01',
       'ob110037' : '-30:33:39.7',
       'ob110310' : '-30:24:35.0',
       'ob110462' : '-29:53:26.3',
       'ob110462_corr' : '-29:53:26.3',
       'ob120169' : '-35:22:28.0',
       'ob140613' : '-28:34:21.6', 
       'ob150029' : '-28:38:41.8', 
       'ob150211' : '-30:58:54.3',
       'ob170019' : '-33:00:04.0', 
       'ob170095' : '-33:08:06.6',
       'ob190017' : '-27:32:49.2',
       'ob170302' : '-34:33:19.3',
       'ob170328' : '-28:44:52.6',
       'ob191000' : '-26:30:15.9',
       'ob191080' : '-27:52:01.4',
       'ob190241' : '-29:39:21.9',
       'kb200101' : '-25:24:28.98',
       'kb200122' : '-34:58:32.27',
       'kb200122_short' : '-34:58:32.27',
       'ob040361' : '-33:46:19.7',
       'ob060095' : '-28:46:32.0',
       'ob020061' : '-27:16:01.8',
       'mb19284'  : '-30:20:12.95',}

# The values in astrom_file are from the latest analysis directories
astrom_file = {'ob120169' : '/u/jlu/work/microlens/OB120169/a_2020_08_18/ob120169_astrom_p5_2020_08_18.fits',
               'ob140613' : '/u/jlu/work/microlens/OB140613/a_2020_08_18/ob140613_astrom_p5_2020_08_18_os.fits',
               'ob150029' : '/u/jlu/work/microlens/OB150029/a_2020_08_18/ob150029_astrom_p4_2020_08_18.fits',
               'ob150211' : '/u/jlu/work/microlens/OB150211/a_2020_08_18/ob150211_astrom_p5_2020_08_18.fits',
               'ob170095' : '/u/jlu/work/microlens/OB170095/a_2021_09_18/notes/ob170095_astrom_p4_2021_09_19.fits'} # TEMP

# The values in astrom_file are from the latest analysis directories
astrom_hst = {'mb09260_f606w'  : '/u/jlu/work/microlens/MB09260/a_2021_07_08/mb09260_f606w_astrom_p4_2021_07_08.fits',
              'mb09260_f814w'  : '/u/jlu/work/microlens/MB09260/a_2021_07_08/mb09260_f814w_astrom_p4_2021_07_08.fits',
              'mb10364_f606w' : '/u/jlu/work/microlens/MB10364/a_2021_07_08/mb10364_f606w_astrom_p5_2021_07_08.fits',
              'mb10364_f814w' : '/u/jlu/work/microlens/MB10364/a_2021_07_08/mb10364_f814w_astrom_p5_2021_07_08.fits',
              'ob110037_f606w' : '/u/jlu/work/microlens/OB110037/a_2021_07_08/ob110037_f606w_astrom_p5_2021_07_08.fits',
              'ob110037_f814w' : '/u/jlu/work/microlens/OB110037/a_2021_07_08/ob110037_f814w_astrom_p5_2021_07_08.fits',
              'ob110310_f606w' : '/u/jlu/work/microlens/OB110310/a_2021_07_08/ob110310_f606w_astrom_p4_2021_07_08.fits',
              'ob110310_f814w' : '/u/jlu/work/microlens/OB110310/a_2021_07_08/ob110310_f814w_astrom_p4_2021_07_08.fits',
              'ob110462_f606w' : '/u/jlu/work/microlens/OB110462/a_2021_07_08/ob110462_f606w_astrom_p5_nomay_2021_07_08.fits',
              'ob110462_f814w' : '/u/jlu/work/microlens/OB110462/a_2021_07_08/ob110462_f814w_astrom_p5_nomay_2021_07_08.fits',
              'ob110462_corr_f606w' : '/u/jlu/work/microlens/OB110462/a_2021_07_08/ob110462_f606w_astrom_p5_nomay_2021_07_08.fits',
              'ob110462_corr_f814w' : '/u/jlu/work/microlens/OB110462/a_2021_07_08/ob110462_f814w_astrom_p5_nomay_2021_07_08.fits',
              'mb19284_f814w'  : '/u/jlu/work/microlens/MB19284/a_2021_08_11_hst_keck/mb19284_astrom_p4_2021_04_10.fits'}

photom_file = {'ob110037' : '/g/lu/data/microlens/ogle/OGLE-2011-BLG-0037.dat',
               'ob110310' : '/g/lu/data/microlens/ogle/OGLE-2011-BLG-0310.dat',
               'ob110462' : '/g/lu/data/microlens/ogle/OGLE-2011-BLG-0462.dat',
               'ob110462_corr' : '/g/lu/data/microlens/ogle/OGLE-2011-BLG-0462_corr.dat',
               'ob120169' : '/g/lu/data/microlens/ogle/v2019_06/OGLE-2012-BLG-0169.dat',
               'ob140613' : '/g/lu/data/microlens/ogle/v2019_06/OGLE-2014-BLG-0613.dat', 
               'ob150029' : '/g/lu/data/microlens/ogle/v2019_06/OGLE-2015-BLG-0029.dat', 
               'ob150211' : '/g/lu/data/microlens/ogle/v2019_06/OGLE-2015-BLG-0211.dat',
               'ob170302' : '/g/lu/data/microlens/ogle/v2020_01_ews/OGLE-2017-BLG-0302.dat',
               'ob170328' : '/g/lu/data/microlens/ogle/v2020_01_ews/OGLE-2017-BLG-0328.dat',
               'ob170019' : '/g/lu/data/microlens/ogle/ews/OB170019.dat',
               'ob170095' : '/g/lu/data/microlens/ogle/ews/OB170095.dat',
               'ob190017' : '/g/lu/data/microlens/ogle/ews/OB190017.dat',
               'ob191000' : '/g/lu/data/microlens/ogle/v2020_01_ews/OGLE-2019-BLG-1000.dat',
               'ob191080' : '/g/lu/data/microlens/ogle/v2020_01_ews/OGLE-2019-BLG-1080.dat',
               'ob190241' : '/g/lu/data/microlens/ogle/v2020_01_ews/OGLE-2019-BLG-0241.dat',
               'ob040361' : '/g/lu/data/microlens/ogle/OGLE-2004-BLG-0361.dat',
               'ob020061' : '/g/lu/data/microlens/ogle/OGLE-2002-BLG-0061.dat',
               'ob060095' : '/g/lu/data/microlens/ogle/OGLE-2006-BLG-0095.dat',}

photom_spitzer = {'ob120169': None,
                  'ob140613': '/g/lu/data/microlens/spitzer/calchi_novati_2015/ob140613_phot_2.txt',
                  'ob150029': '/g/lu/data/microlens/spitzer/calchi_novati_2015/ob150029_phot_2.txt',
                  'ob150211': '/g/lu/data/microlens/spitzer/calchi_novati_2015/ob150211_phot_3.txt'}

photom_moa = {'mb09260' : '/g/lu/data/microlens/moa/MB09260/mb09260-MOA2R-10000.phot.dat',
              'mb10364' : '/g/lu/data/microlens/moa/MB10364/mb10364-MOA2R-10000.phot.dat',
              'mb11039' : '/g/lu/data/microlens/moa/MB11039/mb11039-MOA2R-10000.phot.dat', # OB110037
              'mb11332' : '/g/lu/data/microlens/moa/MB11332/mb11332-MOA2R-10000.phot.dat', # OB110310
              'mb11191' : '/g/lu/data/microlens/moa/MB11191/mb11191-MOA2R-10000.phot.dat', # OB110462
              'mb19284' : '/g/lu/data/microlens/moa/MB19284/MOA-2019-BLG-284.dat'}

photom_kmt = {'kb200101' : '/g/lu/data/microlens/kmtnet/alerts_2020/kb200101/KMTA19_I.pysis.txt',
              'kb200122' : '/g/lu/data/microlens/kmtnet/alerts_2020/kb200122/KMTA37_I.pysis'}

# THIS ONE IS A TEMPORARY HACK... 
photom_kmt_dia = {'kb200122' : '/Users/casey/scratch/proposals/hst28_ddt/kmt_dia.dat',
                  'kb200122_short' : '/Users/casey/scratch/proposals/hst28_ddt/kmt_dia_short.dat'}

data_sets = {'mb09260' : {'MOA'   :      photom_moa['mb09260'],
                          'HST_f606w' :  astrom_hst['mb09260_f606w'],
                          'HST_f814w' :  astrom_hst['mb09260_f814w']},
             'mb10364' : {'MOA'   :      photom_moa['mb10364'],
                          'MOA_TEST'  :  photom_moa['mb10364'],
                          'HST_f606w' :  astrom_hst['mb10364_f606w'],
                          'HST_f814w' :  astrom_hst['mb10364_f814w']},
             'ob110037': {'I_OGLE':      photom_file['ob110037'],
                          'MOA'   :      photom_moa['mb11039'],
                          'HST_f606w' :  astrom_hst['ob110037_f606w'],
                          'HST_f814w' :  astrom_hst['ob110037_f814w']},
             'ob110310': {'I_OGLE':      photom_file['ob110310'],
                          'MOA'   :      photom_moa['mb11332'],
                          'HST_f606w' :  astrom_hst['ob110310_f606w'],
                          'HST_f814w' :  astrom_hst['ob110310_f814w']},
             'ob110462': {'I_OGLE':      photom_file['ob110462'],
                          'MOA'   :      photom_moa['mb11191'],
                          'HST_f606w' :  astrom_hst['ob110462_f606w'],
                          'HST_f814w' :  astrom_hst['ob110462_f814w']},
             'ob110462_corr': {'I_OGLE':      photom_file['ob110462_corr'],
                          'HST_f606w' :  astrom_hst['ob110462_corr_f606w'],
                          'HST_f814w' :  astrom_hst['ob110462_corr_f814w']},
             'ob120169': {'I_OGLE':      photom_file['ob120169'],
                          'Kp_Keck':     astrom_file['ob120169']},
             'ob140613': {'I_OGLE':      photom_file['ob140613'],
                          'Kp_Keck':     astrom_file['ob140613'],
                          'Ch1_Spitzer': photom_spitzer['ob140613']},
             'ob150029': {'I_OGLE':      photom_file['ob150029'],
                          'Kp_Keck':     astrom_file['ob150029'],
                          'Ch1_Spitzer': photom_spitzer['ob150029']},
             'ob150211': {'I_OGLE':      photom_file['ob150211'],
                          'Kp_Keck':     astrom_file['ob150211'],
                          'Ch1_Spitzer': photom_spitzer['ob150211']},
             'ob170302': {'I_OGLE':      photom_file['ob170302']},
             'ob170328': {'I_OGLE':      photom_file['ob170328']},
             'ob170019': {'I_OGLE':      photom_file['ob170019']},
             'ob170095': {'I_OGLE':      photom_file['ob170095'],
                          'Kp_Keck':     astrom_file['ob170095']},
             'ob190017': {'I_OGLE':      photom_file['ob190017']},
             'ob191000': {'I_OGLE':      photom_file['ob191000']},
             'ob191080': {'I_OGLE':      photom_file['ob191080']},
             'ob190241': {'I_OGLE':      photom_file['ob190241']},
             'kb200101': {'KMT'   :      photom_kmt['kb200101']},
             'kb200122': {'KMT'   :      photom_kmt['kb200122'],
                          'KMT_DIA'    : photom_kmt_dia['kb200122']},
             'kb200122_short': {'KMT_DIA'    : photom_kmt_dia['kb200122_short']},
             'ob040361': {'I_OGLE':      photom_file['ob040361']},
             'ob020061': {'I_OGLE':      photom_file['ob020061']},
             'ob060095': {'I_OGLE':      photom_file['ob060095']},
             'mb19284' : {'MOA'   :      photom_moa['mb19284']},}
#                          'HST_f814w' :  astrom_hst['mb19284_f814w']},
#             }
    

def getdata2(target, phot_data=['I_OGLE'], ast_data=['Kp_Keck'],
             time_format='mjd', verbose=False):
    """
    Get the photometric and astrometric data for the specified target. 
    Specify the types of data through the phot_data and ast_data lists. 

    Inputs
    ----------
    target : str
        Target name (lower case)

    Optional Inputs
    --------------------
    phot_data : list
        List of strings specifying the data sets. Options include:
        I_OGLE, Kp_Keck, Ch1_Spitzer, MOA

    ast_data : list
        List of strings specifying the data sets. Options include:
        Kp_Keck

    time_format : string
        The time format (default = 'mjd') such as mjd, year, jd.

    verbose : bool
        Print out extra information. 

    Returns
    ----------
    data : dict
        A ditionary containing the data. For each photometric data set, the dictionary
        contains:
        
            t_phot1
            mag1
            mag_err1

        where the '1' at the end is incremented for additional data sets. Note the
        index is assigned according to the order int he list. Note that if only a single
        photometry data set is requested, the returned keys are t_phot, mag, mag_err
        with a 1 on the end.

        For each astrometric data set, the dictionary contains:
        
            t_ast1
            xpos1
            ypos1
            xpos_err1
            ypos_err1

        where the index is incremented for additional astrometric data sets (useful for the future).

        There are two additional entries in the dictionary which contain the R.A. and Dec.
        of the lensing target... this is the photocenter of the joint lens/source system and 
        is hard-coded in module tables. Note that if only a single
        astrometry data set is requested, the returned keys are t_ast, xpos, ypos, xpos_err, ypos_err
        with no index on the end.

        data['raL']
        data['decL']
    """
    data = {}

    # Load the RA and Dec
    target_coords = SkyCoord(ra[target], dec[target], 
                             unit = (units.hourangle, units.deg), frame = 'icrs')
    data['target'] = target
    data['raL'] = target_coords.ra.degree
    data['decL'] = target_coords.dec.degree

    # Keep track of the data files we used.
    phot_files = []
    ast_files = []
    
    # Load up the photometric data.
    for pp in range(len(phot_data)):
        filt = phot_data[pp]

        if filt not in data_sets[target].keys():
            raise RuntimeError('Failed to find photometric data set {0:s} for {1:s}'.format(filt, target))
        
        phot_files.append(data_sets[target][filt])
                              
        if filt == 'I_OGLE':
            # Read in photometry table.
            pho = Table.read(data_sets[target][filt], format = 'ascii')
            t = Time(pho['col1'], format='jd', scale='utc')
            m = pho['col2']
            me = pho['col3']

        if filt == 'Kp_Keck':
            pho = Table.read(data_sets[target][filt])
            tdx = np.where(pho['name'] == target)[0][0]
            t = Time(pho['t'][tdx, :], format='jyear', scale='utc')
            m = pho['m'][tdx, :]

            # Add empirical photometric errors and radii
            pho['m0e'] = np.nanstd(pho['m'], axis=1)
            pho['dr'] = np.hypot(pho['x0'] - pho['x0'][tdx],
                                 pho['y0'] - pho['y0'][tdx])
            pho['dm'] = pho['m0'] - pho['m0'][tdx]
            
            # We can't use the normal me because it captures the source variability.
            # Calculate from surrounding stars. Don't use the target itself.
            dr = pho['dr']
            dm = np.abs(pho['dm'])

            # Iterate until we get some stars.
            n_neigh = 0
            nn = 1
            dr_start = 2.5
            dm_start = 1.5
            
            while n_neigh < 3:
                r_factor = 1.0 + (nn / 10.)  # Grow search radius by 10% each round.
                m_factor = 1.0 + (nn / 5.)   # Grow mag search by 20% each round.
                rdx = np.where((dr < dr_start*r_factor) & (dm < dm_start*m_factor) & (pho['m0e'] != 0))[0]
                rdx = rdx[rdx != tdx]  # Drop the target.
                n_neigh = len(rdx)
                nn += 1

            # For all the magniudes of the surrounding stars (in individual epochs),
            # mask out the invalid values.
            me_neigh = np.nanmean( pho['m0e'][rdx] )
            if verbose:
                print('Found {0:d} neighbors within:'.format(n_neigh))
                print('  dr = {0:0.2f} arcsec'.format(dr_start * r_factor))
                print('  dm = {0:0.2f} mag'.format(dm_start * m_factor))
                print(pho['name','m0','m0e','dr','dm'][rdx])

            if np.isnan(me_neigh):
                me_neigh = 0.025
                if verbose:
                    print('Using hard-coded me_neigh')

            if verbose: 
                print('me_neigh = {0:.3f} mag'.format(me_neigh))
                
            me = np.ones(len(t), dtype=float) * me_neigh

        if filt == 'Ch1_Spitzer':
            pho = Table.read(data_sets[target][filt], format='ascii')
            t = Time(pho['col1']  + 2450000.0, format='jd', scale='utc')
            f = pho['col2']
            fe = pho['col3']
            m = 25.0 - 2.5 * np.log10(f)
            me = 1.086 * fe / f

        if filt == 'MOA':
            pho = Table.read(data_sets[target][filt], format='ascii')
            # Convert HJD provided by MOA into JD.
            # https://geohack.toolforge.org/geohack.php?pagename=Mount_John_University_Observatory&params=43_59.2_S_170_27.9_E_region:NZ-CAN_type:landmark
            moa = coord.EarthLocation(lat=-43.986667 * u.deg,lon=170.465*u.deg, height=1029*u.meter)
            t_hjd = atime.Time(pho['col1'], format='jd', scale = 'utc')
            ltt = t_hjd.light_travel_time(target_coords, 'heliocentric', location=moa)

            t = t_hjd - ltt
            m = pho['col5']
            me = pho['col6']

        if filt[0:3] == 'HST':
            pho = Table.read(data_sets[target][filt])
            if target == 'ob110462_corr':
                tdx = np.where(pho['name'] == 'OB110462')[0][0]
            else:
                tdx = np.where(pho['name'] == target.upper())[0][0]
            good_idx = np.where(~np.isnan(pho[tdx]['t']))[0] # get rid of nans
            t = Time(pho['t'][tdx, good_idx], format='jyear', scale='utc')
            m = pho['m'][tdx, good_idx]
            me = pho['me'][tdx, good_idx]
            # Make sure t is increasing
            if t[0] > t[-1]:
                t = t[::-1]
                m = m[::-1]
                me = me[::-1]

        if filt == 'KMT':
            pho = Table.read(data_sets[target][filt], format='ascii')
            t = Time(pho['HJD'] + 2450000.0, format='jd', scale='utc')
            m = pho['mag']
            me = pho['mag_err']

        if filt == 'KMT_DIA':
            pho = Table.read(data_sets[target][filt], format='ascii')
            t = Time(pho['col1'] + 2450000.0, format='jd', scale='utc')
            m = 27.68-2.5*np.log10(pho['col2']+27300)
            me = -1.08 * pho['col3']/(pho['col2'] + 27300)

        # Set time to proper format
        if time_format == 'mjd':
            t = t.mjd
        if time_format == 'jyear':
            t = t.j_year
        if time_format == 'jd':
            t = t.jd

        # Insert the data into the dictionary.
        suffix = '{0:d}'.format(pp + 1)
        if len(phot_data) == 1:
            suffix = '1'

        data['t_phot' + suffix] = t
        data['mag' + suffix] = m
        data['mag_err' + suffix] = me

    for aa in range(len(ast_data)):
        filt = ast_data[aa]

        if filt not in data_sets[target].keys():
            raise RuntimeError('Failed to find astrometric data set {0:s} for {1:s}'.format(filt, target))

        ast_files.append(data_sets[target][filt])
        
        if filt == 'Kp_Keck':
            ast = Table.read(data_sets[target][filt])
            tdx = np.where(ast['name'] == target)[0][0]
            t = Time(ast['t'][tdx, :], format='jyear', scale='utc')
            x = ast['x'][tdx, :] * -1.0   # East in +x direction
            y = ast['y'][tdx, :]
            xe = ast['xe'][tdx, :]
            ye = ast['ye'][tdx, :]

        if filt[0:3] == 'HST':
            ast = Table.read(data_sets[target][filt])
            if target == 'ob110462_corr':
                tdx = np.where(ast['name'] == 'OB110462')[0][0]
            else:
                tdx = np.where(ast['name'] == target.upper())[0][0]
            good_idx = np.where(~np.isnan(ast[tdx]['t']))[0] # get rid of nans 
            t = Time(ast['t'][tdx, good_idx], format='jyear', scale='utc')
            x = ast['x'][tdx, good_idx] * -1.0   # East in +x direction
            y = ast['y'][tdx, good_idx]
            xe = ast['xe'][tdx, good_idx]
            ye = ast['ye'][tdx, good_idx]

            # Make sure t is increasing
            if t[0] > t[-1]:
                t = t[::-1]
                x = x[::-1]
                y = y[::-1]
                xe = xe[::-1]
                ye = ye[::-1]
            
        # Set time to proper format
        if time_format == 'mjd':
            t = t.mjd
        if time_format == 'jyear':
            t = t.j_year
        if time_format == 'jd':
            t = t.jd

        # Insert the data into the dictionary.
        suffix = '{0:d}'.format(aa + 1)
            
        data['t_ast' + suffix] = t
        data['xpos' + suffix] = x
        data['ypos' + suffix] = y
        data['xpos_err' + suffix] = xe
        data['ypos_err' + suffix] = ye

    # Keep a record of the types of data.
    data['phot_data'] = phot_data
    data['ast_data'] = ast_data

    data['phot_files'] = phot_files
    data['ast_files'] = ast_files

#    if (target == 'ob110462_corr') & (len(data['ast_files']) > 0):
#        ir_dx = 1E-3 * np.array([0.04590994914109796, 0.20270813855993255, 0.27908995259116326, 0.35875856009576756,
#                                 0.48262772956765027, 0.7147107215435291, 0.288944483266394])
#        
#        ir_dy = 1E-3 * np.array([-0.01256823405333261, -0.06794714789262259, -0.11578369111840361, -0.02792184679700993,
#                                  -0.09577152016290691, -0.11112216615057705, -0.12390124171850343])
#        
#        ir_sigx = 1E-3 * np.array([0.05971418057559921, 0.06206567456045358, 0.07087117633447436, 0.10225090213878256,
#                                   0.13458989321630424, 0.089700718340495, 0.08556130508294131])
#        
#        ir_sigy = 1E-3 * np.array([0.04745112174745842, 0.048577468328797176, 0.07096463782218623, 0.137489385754817,
#                                   0.13347955319714447, 0.10784257501340623, 0.08743743750317869])
#        
#        cdx = np.average(data['xpos1'] - data['xpos2'],
#                         weights=1/np.hypot(data['xpos_err1'], data['xpos_err1']))
#        
#        cdy = np.average(data['ypos1'] - data['ypos2'],
#                         weights=1/np.hypot(data['ypos_err1'], data['ypos_err1']))
#        
#        data['xpos2'] += cdx
#        data['ypos2'] += cdy
#        
#        data['xpos1'] += ir_dx
#        data['ypos1'] += ir_dy
#        data['xpos_err1'] = np.hypot(data['xpos_err1'], ir_sigx)
#        data['ypos_err1'] = np.hypot(data['ypos_err1'], ir_sigy)
#        pdb.set_trace()
#        
#        data['xpos2'] += ir_dx
#        data['ypos2'] += ir_dy
#        data['xpos_err2'] = np.hypot(data['xpos_err2'], ir_sigx)
#        data['ypos_err2'] = np.hypot(data['ypos_err2'], ir_sigy)
            
    return data
    
def getdata(target, use_astrom_file=None, use_photom_file=None, spitzer_photom_file=None, time_format='mjd', use_astrom_phot=False):
    """
    Optional Inputs
    -------
    target : str
        Options are:
        'ob120169'
        'ob140613'
        'ob150029'
        'ob150211'

    astrom_file : str
        File name of an astropy table (FITS) containing the astrometry. Usually 
        output from FlyStar.
    """
    if use_astrom_file is None:
        use_astrom_file = astrom_file[target]
    if use_photom_file is None:
        use_photom_file = photom_file[target]
    if spitzer_photom_file is None:
        spitzer_photom_file = photom_spitzer[target]

    # Read in astrometry table.
    flystar_tab = Table.read(use_astrom_file)

    # Get astrometry for just target.
    tdx = np.where(flystar_tab['name'] == target)[0][0]

    a_t = flystar_tab['t'][tdx, :]
    a_x = flystar_tab['x'][tdx, :] * -1.0 # East in +x direction
    a_y = flystar_tab['y'][tdx, :]
    a_xe = flystar_tab['xe'][tdx, :]
    a_ye = flystar_tab['ye'][tdx, :]

    ast = Table([a_t, a_x, a_y, a_xe, a_ye], 
                names = ('t', 'x', 'y', 'xe', 'ye'))

    # Read in photometry table.
    pho = Table.read(use_photom_file, format = 'ascii')
    pho.rename_column('col1', 't')
    pho.rename_column('col2', 'm')
    pho.rename_column('col3', 'me')
    
    # Read in spitzer photometry table.
    if spitzer_photom_file != None:
        spit = Table.read(spitzer_photom_file, format='ascii')
        spit.rename_column('col1', 't')
        spit.rename_column('col2', 'f')
        spit.rename_column('col3', 'fe')
        sp_t = Time(spit['t'], format='jd', scale='utc')
        

    # Put all the times in MJD and fix tables.
    a_t = Time(ast['t'], format = 'jyear', scale = 'utc')
    p_t = Time(pho['t'], format = 'jd', scale = 'utc')
    
    if time_format=='mjd':
        ast['t'] = a_t.mjd
        pho['t'] = p_t.mjd
    elif time_format=='jyear':
        ast['t'] = a_t.jyear
        pho['t'] = p_t.jyear
    elif time_format=='jd':
        ast['t'] = a_t.jd
        pho['t'] = p_t.jd

    # Get the photometry from the astrometry data set as well.
    a_m = flystar_tab['m'][tdx, :]
    # I got this error from looking at the STD of the surrounding stars.    
    a_me = np.ones(len(a_m), dtype=float) * 0.025
        
    # Prepare data to be fit
    target_coords = SkyCoord(ra[target], dec[target], 
                             unit = (units.hourangle, units.deg), frame = 'icrs')
    
    data = {}
    data['raL'] = target_coords.ra.degree
    data['decL'] = target_coords.dec.degree
    data['t_ast'] = ast['t']
    data['xpos'] = ast['x']
    data['ypos'] = ast['y']
    data['xpos_err'] = ast['xe']
    data['ypos_err'] = ast['ye']

    if use_astrom_phot == False:
        data['t_phot1'] = pho['t']
        data['mag1'] = pho['m']
        data['mag_err1'] = pho['me']
    else:
        data['t_phot1'] = pho['t']
        data['mag1'] = pho['m']
        data['mag_err1'] = pho['me']
        data['t_phot2'] = ast['t']
        data['mag2'] = a_m
        data['mag_err2'] = a_me

    return data 

def getdata_OGLEphot(phot_file, ra, dec, time_format='mjd', add_tconst = True):
    """
    Set up OGLE photometry to be fit, given some file.
    (This is mostly for OGLE EWS stuff where we don't
    have any astrometry available.)
    """
    # Read in photometry table.
    pho = Table.read(phot_file, format = 'ascii')
    pho.rename_column('col1', 't')
    pho.rename_column('col2', 'm')
    pho.rename_column('col3', 'me')

    # Put all the times in MJD and fix tables.
    if add_tconst is True:
        # For OGLE-III EWS
        p_t = Time(pho['t'] + 2450000, format = 'jd', scale = 'utc')

    if add_tconst is False:
        # For OGLE-IV EWS
        p_t = Time(pho['t'], format = 'jd', scale = 'utc')
    
    if time_format=='mjd':
        pho['t'] = p_t.mjd

    # Prepare data to be fit
    target_coords = SkyCoord(ra, dec, 
                             unit = (units.hourangle, units.deg), frame = 'icrs')
    
    data = {}
    data['raL'] = target_coords.ra.degree
    data['decL'] = target_coords.dec.degree
    data['t_phot1'] = pho['t']
    data['mag1'] = pho['m']
    data['mag_err1'] = pho['me']
        
    return data 


###################################
# OLD STUFF DON'T USE THIS HERE
# KEEPING SO OLD CODE DOESN'T BREAK
###################################

def getdata_photonly(target, use_photom_file=None, time_format='mjd'):
    """
    Optional Inputs
    -------
    target : str
        Options are:
        'ob120169'
        'ob140613'
        'ob150029'
        'ob150211'

    astrom_file : str
        File name of an astropy table (FITS) containing the astrometry. Usually 
        output from FlyStar.
    """
    if use_photom_file is None:
        use_photom_file = photom_file[target]

    # Read in photometry table.
    pho = Table.read(use_photom_file, format = 'ascii')
    pho.rename_column('col1', 't')
    pho.rename_column('col2', 'm')
    pho.rename_column('col3', 'me')

    # Put all the times in MJD and fix tables.
    p_t = Time(pho['t'], format = 'jd', scale = 'utc')
    
    if time_format=='mjd':
        pho['t'] = p_t.mjd

    # Prepare data to be fit
    target_coords = SkyCoord(ra[target], dec[target], 
                             unit = (units.hourangle, units.deg), frame = 'icrs')
    
    data = {}
    data['raL'] = target_coords.ra.degree
    data['decL'] = target_coords.dec.degree
    data['t_phot1'] = pho['t']
    data['mag1'] = pho['m']
    data['mag_err1'] = pho['me']
        
    return data 

# FOR DEBUGGING
def getdata_keckonly(target, time_format='mjd'):
    """
    Optional Inputs
    -------
    target : str
        Options are:
        'ob120169'
        'ob140613'
        'ob150029'
        'ob150211'

    astrom_file : str
        File name of an astropy table (FITS) containing the astrometry. Usually 
        output from FlyStar.
    """
    use_astrom_file = astrom_file[target]

    # Read in astrometry table.
    flystar_tab = Table.read(use_astrom_file)

    # Get astrometry for just target.
    tdx = np.where(flystar_tab['name'] == target)[0][0]

    a_t = flystar_tab['t'][tdx, :]
    a_x = flystar_tab['x'][tdx, :] * -1.0 # East in +x direction
    a_y = flystar_tab['y'][tdx, :]
    a_xe = flystar_tab['xe'][tdx, :]
    a_ye = flystar_tab['ye'][tdx, :]

    ast = Table([a_t, a_x, a_y, a_xe, a_ye], 
                names = ('t', 'x', 'y', 'xe', 'ye'))

    # Put all the times in MJD and fix tables.
    a_t = Time(ast['t'], format = 'jyear', scale = 'utc')
    
    if time_format=='mjd':
        ast['t'] = a_t.mjd

    # Get the photometry from the astrometry data set as well.
    a_m = flystar_tab['m'][tdx, :]
    # I got this error from looking at the STD of the surrounding stars.    
    a_me = np.ones(len(a_m), dtype=float) * 0.025
        
    # Prepare data to be fit
    target_coords = SkyCoord(ra[target], dec[target], 
                             unit = (units.hourangle, units.deg), frame = 'icrs')
    
    data = {}
    data['raL'] = target_coords.ra.degree
    data['decL'] = target_coords.dec.degree
    data['t_ast'] = ast['t']
    data['xpos'] = ast['x']
    data['ypos'] = ast['y']
    data['xpos_err'] = ast['xe']
    data['ypos_err'] = ast['ye']
    data['t_phot1'] = ast['t']
    data['mag1'] = a_m
    data['mag_err1'] = a_me

    return data 

