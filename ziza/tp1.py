from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    data = {3,7,7,8,9}
    comm.send(data, dest=1, tag=11)
    print(f"Process {rank} sent data: {data}")
elif rank == 1:
    data = comm.recv(source=0, tag=11)
    print(f"Process {rank} received data: {data}")

print(f"Process {rank} out of {size} is done.")
