{ 
  SaveState (); 
  InitSpecificTime (&t_speedup_cpu, ""); 
  for (t_speedup_count=0; t_speedup_count < 200; t_speedup_count++) { 
    SubStep1_x_cpu (dt); 
  } 
  time_speedup_cpu = GiveSpecificTime (t_speedup_cpu);
  RestoreState (); 
  InitSpecificTime (&t_speedup_gpu, ""); 
  for (t_speedup_count=0; t_speedup_count < 2000; t_speedup_count++) { 
    SubStep1_x_gpu (dt);
  }
  time_speedup_gpu = GiveSpecificTime (t_speedup_gpu);
  printf ("GPU/CPU speedup in %s: %g\n", "SubStep1_x", time_speedup_cpu/time_speedup_gpu*10.0);
  printf ("CPU time : %g ms\n", 1e3*time_speedup_cpu/200.0); 
  printf ("GPU time : %g ms\n", 1e3*time_speedup_gpu/2000.0);
};

 { 
   SaveState ();
   printf ("Executing %s_cpu%s\n","Edamp","(dt)");
   Edamp_cpu (dt);
   DumpAllFields (999);
   SaveStateSecondary ();
   RestoreState ();
   printf ("Executing %s_gpu%s\n","Edamp","(dt)"); 
   Edamp_gpu (dt); 
   DumpAllFields (998);
   CompareAllFields (); 
   prs_exit (0); 
  };
