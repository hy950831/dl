import pickle
from capdl.Spec import Spec
from capdl.Object import CNode, Endpoint, Frame, TCB, PML4
from capdl.Cap import Cap
from capdl.Allocator import ObjectAllocator, CSpaceAllocator, AddressSpaceAllocator


cnode_program_1 = CNode("cnode_program_1", 2) # A CNode which has 3 slots
cnode_program_2 = CNode("cnode_program_2", 2) # A CNode which has 3 slots
cnode_shared_lib = CNode("cnode_shared_lib", 2)

shared_frame_obj = Frame("shared_frame_obj", 4096)

ep = Endpoint("endpoint")

cnode_program_1["0x1"] = Cap(cnode_program_1)
cnode_program_1["0x2"] = Cap(ep, read=True, write=True, grant=True)

cnode_program_2["0x1"] = Cap(cnode_program_2)
cnode_program_2["0x2"] = Cap(ep, read=True, write=True, grant=True)

cnode_shared_lib["0x1"] = Cap(cnode_shared_lib)

ipc_program_1_obj = Frame("ipc_program_1_obj", 4096)
ipc_program_2_obj = Frame("ipc_program_2_obj", 4096)

vspace_program_1 = PML4("vspace_program_1")
vspace_program_2 = PML4("vspace_program_2")
vspace_shared = PML4("vspace_shared")

tcb_program_1 = TCB("tcb_program_1",
                    ipc_buffer_vaddr= 0x0,
                    ip= 0x0,
                    sp= 0x0,
                    elf= "program_1",
                    prio= 254,
                    max_prio= 254,
                    affinity= 0,
                    init= []
                    )

tcb_program_2 = TCB("tcb_program_2",
                    ipc_buffer_vaddr= 0x0,
                    ip= 0x0,
                    sp= 0x0,
                    elf= "program_2",
                    prio= 254,
                    max_prio= 254,
                    affinity= 0,
                    init= []
                    )

tcb_shared = TCB("tcb_shared",
                     ipc_buffer_vaddr= 0x0,
                     ip= 0x0,
                     sp= 0x0,
                     elf= "libshared.so",
                     prio= 0,
                     max_prio= 0,
                     affinity= 0,
                     init= []
                     )

tcb_program_1['cspace'] = Cap(cnode_program_1)
tcb_program_1['vspace'] = Cap(vspace_program_1)
tcb_program_1['ipc_buffer_slot'] = Cap(ipc_program_1_obj, read=True, write=True)

tcb_program_2['cspace'] = Cap(cnode_program_2)
tcb_program_2['vspace'] = Cap(vspace_program_2)
tcb_program_2['ipc_buffer_slot'] = Cap(ipc_program_2_obj, read=True, write=True)

tcb_shared['cspace'] = Cap(cnode_shared_lib)
tcb_shared['vspace'] = Cap(vspace_shared)

stack_0_program_1_obj = Frame("stack_0_program_1_obj", 4096)
stack_1_program_1_obj = Frame("stack_1_program_1_obj", 4096)
stack_2_program_1_obj = Frame("stack_2_program_1_obj", 4096)
stack_3_program_1_obj = Frame("stack_3_program_1_obj", 4096)
stack_4_program_1_obj = Frame("stack_4_program_1_obj", 4096)
stack_5_program_1_obj = Frame("stack_5_program_1_obj", 4096)
stack_6_program_1_obj = Frame("stack_6_program_1_obj", 4096)
stack_7_program_1_obj = Frame("stack_7_program_1_obj", 4096)
stack_8_program_1_obj = Frame("stack_8_program_1_obj", 4096)
stack_9_program_1_obj = Frame("stack_9_program_1_obj", 4096)

stack_0_program_2_obj = Frame("stack_0_program_2_obj", 4096)
stack_1_program_2_obj = Frame("stack_1_program_2_obj", 4096)
stack_2_program_2_obj = Frame("stack_2_program_2_obj", 4096)
stack_3_program_2_obj = Frame("stack_3_program_2_obj", 4096)
stack_4_program_2_obj = Frame("stack_4_program_2_obj", 4096)
stack_5_program_2_obj = Frame("stack_5_program_2_obj", 4096)
stack_6_program_2_obj = Frame("stack_6_program_2_obj", 4096)
stack_7_program_2_obj = Frame("stack_7_program_2_obj", 4096)
stack_8_program_2_obj = Frame("stack_8_program_2_obj", 4096)
stack_9_program_2_obj = Frame("stack_9_program_2_obj", 4096)

obj = set([
cnode_program_1,
cnode_program_2,
cnode_shared_lib,
ep,
ipc_program_1_obj,
ipc_program_2_obj,
stack_0_program_1_obj,
stack_0_program_2_obj,
stack_1_program_1_obj,
stack_1_program_2_obj,
stack_2_program_1_obj,
stack_2_program_2_obj,
stack_3_program_1_obj,
stack_3_program_2_obj,
stack_4_program_1_obj,
stack_4_program_2_obj,
stack_5_program_1_obj,
stack_5_program_2_obj,
stack_6_program_1_obj,
stack_6_program_2_obj,
stack_7_program_1_obj,
stack_7_program_2_obj,
stack_8_program_1_obj,
stack_8_program_2_obj,
stack_9_program_1_obj,
stack_9_program_2_obj,
vspace_program_1,
vspace_program_2,
vspace_shared,
tcb_program_1,
tcb_program_2,
tcb_shared,
shared_frame_obj,
])

spec = Spec('x86_64')
spec.objs = obj
objects = ObjectAllocator()
objects.spec.arch  = 'x86_64'
objects.counter = 37
objects.merge(spec)

program_1_alloc = CSpaceAllocator(cnode_program_1)
program_1_alloc.slot = 4
program_2_alloc = CSpaceAllocator(cnode_program_2)
program_2_alloc.slot = 4

# Shared lib cspace allocator
shared_lib_alloc = CSpaceAllocator(cnode_shared_lib)
shared_lib_alloc.slot = 2

cspaces = {
    'program_1':program_1_alloc,
    'program_2': program_2_alloc,
    'shared': shared_lib_alloc
}

shared_addr_alloc = AddressSpaceAllocator('addr allocator libshared.so', vspace_shared)
shared_addr_alloc._symbols = {}

program_1_addr_alloc = AddressSpaceAllocator('addr allocator 1', vspace_program_1)
program_1_addr_alloc._symbols = {
'mainIpcBuffer': ([4096], [Cap(ipc_program_1_obj, read=True, write=True)]),
'sharedFrame': ([4096], [Cap(shared_frame_obj, read=True, write=True)]),
'stack': (
    [4096, 4096, 4096, 4096, 4096, 4096, 4096, 4096, 4096, 4096],
	[Cap(stack_0_program_1_obj, read=True, write=True),
	 Cap(stack_1_program_1_obj, read=True, write=True),
	 Cap(stack_2_program_1_obj, read=True, write=True),
	 Cap(stack_3_program_1_obj, read=True, write=True),
	 Cap(stack_4_program_1_obj, read=True, write=True),
	 Cap(stack_5_program_1_obj, read=True, write=True),
	 Cap(stack_6_program_1_obj, read=True, write=True),
	 Cap(stack_7_program_1_obj, read=True, write=True),
	 Cap(stack_8_program_1_obj, read=True, write=True),
	 Cap(stack_9_program_1_obj, read=True, write=True),
    ]),
}


program_2_addr_alloc = AddressSpaceAllocator('addr allocator 2', vspace_program_2)
program_2_addr_alloc._symbols = {
'mainIpcBuffer': ([4096], [Cap(ipc_program_2_obj, read=True, write=True)]),
'sharedFrame': ([4096], [Cap(shared_frame_obj, read=True, write=True)]),
'stack': (
    [4096, 4096, 4096, 4096, 4096, 4096, 4096, 4096, 4096, 4096],
	[Cap(stack_0_program_2_obj, read=True, write=True),
	 Cap(stack_1_program_2_obj, read=True, write=True),
	 Cap(stack_2_program_2_obj, read=True, write=True),
	 Cap(stack_3_program_2_obj, read=True, write=True),
	 Cap(stack_4_program_2_obj, read=True, write=True),
	 Cap(stack_5_program_2_obj, read=True, write=True),
	 Cap(stack_6_program_2_obj, read=True, write=True),
	 Cap(stack_7_program_2_obj, read=True, write=True),
	 Cap(stack_8_program_2_obj, read=True, write=True),
	 Cap(stack_9_program_2_obj, read=True, write=True),
    ]),
}


addr_spaces = {
    'program_1': program_1_addr_alloc,
 	'program_2': program_2_addr_alloc,
 	'shared': shared_addr_alloc,
               }

cap_symbols = {
    'program_1':
	    [('endpoint', 1),
	     ('cnode', 2),
        ],
    'program_2':
	    [('endpoint', 1),
	     ('cnode', 2),
        ],
    'shared':
        [],
               }


region_symbols = {
    'program_1': [
        ('stack', 4096 * 10, '.bss'),
        ('mainIpcBuffer', 4096, '.bss'),
        ('sharedFrame', 4096, '.bss'),
        ('sharedLibFrame', 4096 * 2000, '.bss')
    ],
    'program_2': [
        ('stack', 4096 * 10, '.bss'),
        ('mainIpcBuffer', 4096, '.bss'),
        ('sharedFrame', 4096, '.bss'),
        ('sharedLibFrame', 4096 * 2000, '.bss')
    ],
    'shared': [
        # FIXME: Currently this thing(allocate region sym) is done
        # by cdl_pp  where the region symbols are defined in a generated c
        # file and the generated c file is depended on sel4 and other
        # libraries which are statically compiled which couldn't be linked
        # with the so file(Even if we can then the dynamic linking is
        # then meaningless by statically linking everything into the elf)
        #  ('stack', 4096 * 4, 'size_12bit'),
    ]
}

elfs =  {
    'program_1': {'passive': False, 'filename': 'program_1.c'},
    'program_2': {'passive': False, 'filename': 'program_2.c'},
    'libshared.so': {'passive': False, 'filename': 'lib/set.c'}
         }


print(pickle.dumps((objects, cspaces, addr_spaces, cap_symbols, region_symbols, elfs)))

