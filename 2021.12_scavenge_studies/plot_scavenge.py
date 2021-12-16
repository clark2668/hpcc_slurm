import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import warnings
import time
import datetime
import ROOT
from ROOT import TTimeStamp, gStyle

senior = ['baclark', 'drg', 'hallid15', 'koppercl', 'nisamehr', 'tdeyoung']
grads = ['harnisc6', 'lehieu1', 'micall12', 'nowick70', 'peiskera', 'rysewykd', 'salaza82', 'sanch373', 'twagiray']
ugrads = ['kowal165', 'kowalc40', 'nguye639', 'priesbr1']
total = [senior, grads, ugrads]

senior = ['baclark']
total = [senior]


gStyle.SetOptStat(0)

h1_num_preemptions = ROOT.TH1D("h1_num_preemptions", "Number of Pre-Empted 'Parent' Jobs", 20,-0.5,19.5)
h1_num_preemptions.GetXaxis().SetTitle("Number of Pre-Emptions")
h1_num_preemptions.GetYaxis().SetTitle("Number of 'Parent' Jobs")

h1_preemption_length = ROOT.TH1D("h1_preemption_length", "Length of Pre-Empted Job Instances", 50, 0, 4*60)
h1_preemption_length.GetXaxis().SetTitle("Job Duration [min]")
h1_preemption_length.GetYaxis().SetTitle("Number of Pre-Empted Job Instances")

h1_completion_length = ROOT.TH1D("h1_completion_length", "Length of Completed Job Instances", 50, 0, 4*60)
h1_completion_length.GetXaxis().SetTitle("Job Duration [min]")
h1_completion_length.GetYaxis().SetTitle("Number of Completed Jobs")


job_db = {} # start a job database

for group in total:
    for user in group:
        print("on user %s"%user)
        title = "./2021_12_16/log_2021_12_16_%s.txt"%user
        data = np.genfromtxt(title,
                    # delimiter="|",
                    skip_header=0,
                    dtype=[('username','<U8'),('jobid','<i8'),('jobname','<U8'),('status','<U13'),('time','<i8'),('cpus','<i8'),('start','<U24')])
        
        for this_jobid, this_status, this_runtime in zip(data['jobid'], data['status'], data['time']):
            this_status = str(this_status)
            if this_jobid in job_db:
                # update the entry
                # print("Update job {}".format(this_jobid))
                
                job_db[this_jobid]['n_tries'] +=1 

                if(this_status == 'PREEMPTED'):
                    job_db[this_jobid]['preemptions'].append(this_runtime)
                if(this_status == 'COMPLETED'):
                    job_db[this_jobid]['completion_time'] = this_runtime

            else:
                # print('create entry for job {}'.format(this_jobid))
                # create an entry
                job_db[this_jobid] = {}
                
                # counter for number of tries
                job_db[this_jobid]['n_tries'] = 0
                job_db[this_jobid]['n_tries'] +=1 

                # holder for pre-emptions
                job_db[this_jobid]['preemptions'] = []
                if(this_status == 'PREEMPTED'):
                    job_db[this_jobid]['preemptions'].append(this_runtime)
                if(this_status == 'COMPLETED'):
                    job_db[this_jobid]['completion_time'] = this_runtime
                            
        num_jobs_tot = 0
        num_jobs_preempted = 0
        for this_jobid in job_db:
            num_jobs_tot+=1
            if(job_db[this_jobid]['n_tries']>1):
                num_jobs_preempted+=1
            print("For job {}, N Tries is {} ({})".format(this_jobid, job_db[this_jobid]['n_tries'], job_db[this_jobid]['preemptions']))
            h1_num_preemptions.Fill(job_db[this_jobid]['n_tries']-1)
            if 'completion_time' in job_db[this_jobid]:
                h1_completion_length.Fill(job_db[this_jobid]['completion_time']/60.)
            for i in job_db[this_jobid]['preemptions']:
                  h1_preemption_length.Fill(i/60.)
        
        print("Num Total Jobs {}, Num Jobs Pre-Empted {}, Fraction Pre-Empted {:.2f}".format(num_jobs_tot, num_jobs_preempted, num_jobs_preempted/num_jobs_tot))

c3 = ROOT.TCanvas("canvas", "canvas", 1100, 850)
c3.cd()
h1_num_preemptions.Draw("hist")
h1_num_preemptions.SetLineWidth(3)
c3.SetLogy()
c3.Print("num_preemptions.png")


# get the CDF
h1_preemption_length_clone = h1_preemption_length.Clone()
h1_preemption_length_clone.Sumw2()
scale = 1./h1_preemption_length_clone.Integral()
h1_preemption_length_clone.Scale(scale)
h1_preemption_length_cdf = h1_preemption_length_clone.GetCumulative()
h1_preemption_length_cdf.GetYaxis().SetTitle("CDF")

c4 = ROOT.TCanvas("canvas4", "canvas4", 1100*2, 850)
c4.cd()
c4.Divide(2,1)
c4.cd(1)
h1_preemption_length.Draw("hist")
h1_preemption_length.SetLineWidth(3)
c4.cd(2)
h1_preemption_length_cdf.Draw("hist")
h1_preemption_length_cdf.SetLineWidth(3)

c4.SetLogy()
c4.Print("preempted_job_length.png")

c5 = ROOT.TCanvas("canvas4", "canvas4", 1100, 850)
c5.cd()
h1_completion_length.Draw("hist")
h1_completion_length.SetLineWidth(3)
c5.SetLogy()
c5.Print("completed_job_length.png")
