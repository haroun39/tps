from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()   # رقم العملية (0,1,2,3)
size = comm.Get_size()   # عدد العمليات (4 متوقع)

# فقط العملية 0 تُنشئ الجدول
if rank == 0:
    # يمكن إدخال الأرقام يدويًا أو توليدها
    data = [4,9,2,8,6,5,3,1,7,9,10,12,14,16,8,7,2,18,9,7]
    print("\nComplete array:", data)

     # تقسيم الجدول إلى 4 أجزاء متساوية
    chunks = [data[i:i + 5] for i in range(0, 20, 5)]

     # تقسيم الجدول إلى عدد الأجزاء = عدد العمليات
    # n = len(data)
    # chunk_size = n // size
    # chunks = [data[i*chunk_size : (i+1)*chunk_size] for i in range(size)]

    # # إذا لم يتقسم بالتساوي (مثلاً 20/6)، نضيف الباقي لآخر جزء
    # remainder = n % size
    # if remainder:
    #     chunks[-1].extend(data[-remainder:])
else:
    chunks = None

# توزيع الأجزاء على العمليات
part = comm.scatter(chunks, root=0)

# كل عملية تحسب أكبر قيمة في الجزء الخاص بها
local_max = max(part)
print(f"Process {rank} received {part} -> Local max = {local_max}")

# كل عملية تحسب أكبر قيمة في الجزء الخاص بها
all_max = comm.gather(local_max, root=0)
# العملية 0 تبحث عن أكبر قيمة نهائية
if rank == 0:
    print("all_max in process", rank, ":", all_max)
    global_max = max(all_max)
    print("\n--- Summary ---")
    for i, m in enumerate(all_max):
        print(f"Max of process {i} = {m}")
    print(f"\nThe global maximum is: {global_max}")
