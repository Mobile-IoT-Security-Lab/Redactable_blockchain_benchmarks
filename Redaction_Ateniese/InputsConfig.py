import random

class InputsConfig:

    """ Select the model to be simulated.
    0 : The base model
    1 : Bitcoin model
    2 : Ethereum model
    """
    model = 1

    ''' Input configurations for the base model '''
    # if model == 0:
    #
    #     ''' Block Parameters '''
    #     Binterval = 600  # Average time (in seconds)for creating a block in the blockchain
    #     Bsize = 1.0  # The block size in MB
    #     Bdelay = 0.42  # average block propogation delay in seconds, #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
    #     Breward = 12.5  # Reward for mining a block
    #
    #     ''' Transaction Parameters '''
    #     hasTrans = True  # True/False to enable/disable transactions in the simulator
    #     Ttechnique = "Light"  # Full/Light to specify the way of modelling transactions
    #     Tn = 10  # The rate of the number of transactions to be created per second
    #     # The average transaction propagation delay in seconds (Only if Full technique is used)
    #     Tdelay = 5.1
    #     Tfee = 0.000062  # The average transaction fee
    #     Tsize = 0.000546  # The average transaction size  in MB
    #
    #     ''' Node Parameters '''
    #     NUM_NODES = 15  # the total number of nodes in the network
    #     NODES = []
    #     from Models.Node import Node
    #     # here as an example we define three nodes by assigning a unique id for each one
    #     NODES = [Node(id=0, hashPower=50), Node(id=1, hashPower=0), Node(id=2, hashPower=0),
    #              Node(id=3, hashPower=150), Node(id=4, hashPower=50), Node(id=5, hashPower=150),
    #              Node(id=6, hashPower=0), Node(id=7, hashPower=100), Node(id=8, hashPower=0),
    #              Node(id=9, hashPower=0),Node(id=10, hashPower=0), Node(id=11, hashPower=0),
    #              Node(id=12, hashPower=0), Node(id=13, hashPower=0), Node(id=14, hashPower=100)]
    #
    #     ''' Simulation Parameters '''
    #     simTime = 100000  # the simulation length (in seconds)
    #     Runs = 1  # Number of simulation runs

    ''' Input configurations for Bitcoin model '''
    if model == 1:
        ''' Block Parameters '''
        Binterval = 600  # Average time (in seconds)for creating a block in the blockchain
        Bsize = 1.0  # The block size in MB
        Bdelay = 0.42  # average block propogation delay in seconds, #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
        Breward = 12.5  # Reward for mining a block
        Rreward = 0.03  # Reward for redacting a transaction

        ''' Transaction Parameters '''
        hasTrans = True  # True/False to enable/disable transactions in the simulator
        Ttechnique = "Light"  # Full/Light to specify the way of modelling transactions
        Tn = 5  # The rate of the number of transactions to be created per second

        Tdelay = 5.1 # The average transaction propagation delay in seconds (Only if Full technique is used)
        Tfee = 0.001  # The average transaction fee
        Tsize = 0.0006  # The average transaction size in MB

        ''' Node Parameters '''
        NUM_NODES = 1000  # the total number of nodes in the network
        NODES = []
        MINERS_PORTION = 0.3 # Example: 0.5 ==> 50% of miners
        MAX_HASH_POWER = 200
        from Models.Bitcoin.Node import Node
        num_miners = int(NUM_NODES * MINERS_PORTION)

        # Create miners
        for i in range(num_miners):
            hash_power = random.randint(1, MAX_HASH_POWER)
            NODES.append(Node(id=i, hashPower=hash_power))
        # Create regular nodes
        for i in range(num_miners, NUM_NODES):
            NODES.append(Node(id=i, hashPower=0))

        ''' Simulation Parameters '''
        simTime = 100000  # the simulation length (in seconds)
        Runs = 1  # Number of simulation runs

        ''' Redaction Parameters'''
        hasRedact = True
        hasMulti = True
        redactRuns = 1
        adminNode = random.randint(0, len(NODES))
        # adminNode = 50
        
        ''' Smart Contract Parameters '''
        hasSmartContracts = True  # Enable smart contract functionality
        DEPLOYED_CONTRACTS = []  # List of deployed contract addresses
        contractDeploymentRate = 0.05  # Rate of contract deployment per block
        
        ''' Permission Parameters '''
        hasPermissions = True  # Enable permissioned blockchain features
        PERMISSION_LEVELS = {
            "ADMIN": 100,
            "REGULATOR": 80, 
            "MINER": 60,
            "USER": 40,
            "OBSERVER": 20
        }
        
        # Assign roles to nodes
        NODE_ROLES = {}
        num_admins = max(1, len(NODES) // 100) if len(NODES) > 0 else 1
        num_regulators = max(1, len(NODES) // 50) if len(NODES) > 0 else 1
        
        # Simple role assignment without complex dependencies
        admin_count = 0
        regulator_count = 0
        
        for i, node in enumerate(NODES):
            if admin_count < num_admins:
                NODE_ROLES[i] = "ADMIN"
                admin_count += 1
            elif regulator_count < num_regulators:
                NODE_ROLES[i] = "REGULATOR"
                regulator_count += 1
            elif node.hashPower > 0:
                NODE_ROLES[i] = "MINER"
            else:
                NODE_ROLES[i] = random.choice(["USER", "OBSERVER"])
        
        ''' Privacy and Compliance Parameters '''
        hasPrivacyLevels = True
        dataRetentionPeriod = 86400 * 365  # 1 year in seconds
        requireRedactionApproval = True
        minRedactionApprovals = 2  # Minimum approvals for redaction
        
        ''' Smart Contract Redaction Policies '''
        REDACTION_POLICIES = [
            {
                "policy_id": "GDPR_COMPLIANCE",
                "policy_type": "DELETE",
                "conditions": {"privacy_request": True, "data_expired": True},
                "authorized_roles": ["ADMIN", "REGULATOR"],
                "min_approvals": 2,
                "time_lock": 86400  # 24 hours
            },
            {
                "policy_id": "FINANCIAL_AUDIT",
                "policy_type": "ANONYMIZE", 
                "conditions": {"audit_required": True},
                "authorized_roles": ["ADMIN", "REGULATOR"],
                "min_approvals": 3,
                "time_lock": 86400 * 7  # 7 days
            },
            {
                "policy_id": "SECURITY_INCIDENT",
                "policy_type": "MODIFY",
                "conditions": {"security_breach": True},
                "authorized_roles": ["ADMIN"],
                "min_approvals": 1,
                "time_lock": 0  # Immediate
            }
        ]

