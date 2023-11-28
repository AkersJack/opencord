import json
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from cryptography.x509.general_name import IPAddress
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
# For generating the PEM key 
from Crypto.Util.asn1 import DerSequence
# from Crypto.PublicKey import RSA
from binascii import a2b_base64

# For generating a "x509" certificate
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
import uuid
import ipaddress
import urllib.request

"""
<---------------------- Steps ---------------------->
1. You generate a private/public key pair 

2. You create a request for a certificate, which is signed by your key (to 
prove that you own the key). 

3. You give the certificate signing request (CSR) to a Cirtificate Authority (CA)
(don't give them your private key). 

4. The CA validates that you own the resource (e.g. domain) that you want a 
certificate for. 

5. The CA gives you a certificate, signed by them, which identifies your public key, 
and the resource you are authenticated for. 

6. You configure your server to use that certificate, combined with your private key, 
to serve traffic. 


"""


# Old generate (not going to use this one)
def generatePEM_old():
    key = RSA.generate(2048)
    pv_key_string = key.exportKey()
    with open("private.pem", "w") as prv_file:
        print("{}".format(pv_key_string.decode()), file=prv_file)

    pb_key_string = key.exportKey()
    with open("public.pem", "w") as pub_file:
        print("{}".format(pb_key_string.decode()), file=pub_file)

    tp_path = "public.pem"
    with open(tp_path, "rb") as key_file:
        public_key_tp = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
            # password=None, # If the key is a private key and is password protected, provide the password
        )


# The correct generate
def generatePEM(pub_key_path=None, pv_key_path=None):
    key = RSA.generate(2048)

    # Generate the RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    if pv_key_path is None:
        pv_key_path = "./keys/private.pem"
    # Save the private key to a file 
    with open(pv_key_path, "wb") as private_key_file:
        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        private_key_file.write(private_key_bytes)

    # Extract the corresponding public key 
    public_key = private_key.public_key()

    if pub_key_path is None:
        pub_key_path = "./keys/public.pem"
    # Save the public key to a file 
    with open(pub_key_path, "wb") as public_key_file:
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        public_key_file.write(public_key_bytes)


# Use to load keys 
def loadKeys(public_key=None, private_key=None, password=None):
    pubk = None
    privk = None
    if public_key is not None:
        with open(public_key, "rb") as key_file:
            pubk = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
                # password=None, # If the key is a private key and is password protected, provide the password
            )
    if private_key is not None:
        with open(private_key, "rb") as key_file:
            privk = serialization.load_pem_private_key(
                key_file.read(),
                password=password,  # If the private key is password-protect provide the password
                backend=default_backend()
            )

    # Public key always first 

    return pubk, privk


# Use to generate the Cert
"""
# public_key = Public key location 
# private_key = Private key location
# password = password for private key encryption 
# location = cert output location 
# ip = ip for the user otherwise just get it automatically 
# duration = How long the certificate will be valid for (default 30 days)
# uid = Users Unique identifier
"""


def generateCert(public_key=None, private_key=None, password=None, location=None, ip=None, duration=30, uid=None):
    if ip == None:
        ip = urllib.request.urlopen("https://checkip.amazonaws.com").read().decode("utf-8").strip()
    ip = int(ipaddress.ip_address(ip))
    # ip = ipaddress.ip_address(ip) # convert it back to an ip address
    print(f"IP: {ip}")

    # key = rsa.generate_private_key(

    # public_exponent=65537,
    # key_size=2048,
    # )
    if uid == None:
        id = str(uuid.uuid4())
    else:
        id = uid
    # Write our key to disk for safe keeping

    # with open("private.pem", "wb") as f:

    #     f.write(key.private_bytes(

    #         encoding=serialization.Encoding.PEM,

    #         format=serialization.PrivateFormat.TraditionalOpenSSL,

    #         encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase"),

    #     ))

    subject = x509.Name([
        x509.NameAttribute(NameOID.USER_ID, id),
    ])

    issuer = x509.Name([
        # x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        # x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Maryland"),
        # x509.NameAttribute(NameOID.LOCALITY_NAME, u"Baltimore"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"opencord"),  # Organization Name
        x509.NameAttribute(NameOID.COMMON_NAME, u"opencord.chat"),  # Website of Organization
    ])

    keys = loadKeys(private_key=private_key, public_key=public_key)
    pub_key = keys[0]
    priv_key = keys[1]

    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        # key.public_key()
        pub_key
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc)
    ).not_valid_after(
        # Our certificate will be valid for 30 days (default) or whatever duration is set to 
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=duration)
    ).add_extension(
        # x509.SubjectAlternativeName([x509.DNSName(u"localhost")]), 
        x509.SubjectAlternativeName([x509.IPAddress(ipaddress.ip_address(ip))]),
        critical=False,
    ).sign(priv_key, hashes.SHA256())  # Sign our certificate with our private key

    with open(location, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    return cert


# x509.NameAttribute(x509.ObjectIdentifier("2.999.1"), "value1"),

# To generage a CSR however we will probably not do it this way 
def csr(key):
    # Certificate signing request 
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        # Provide various details about who we are. 
        x509.NameAttribute(NameOID.EMAIL_ADDRESS, u"example@example.com"),
        x509.NameAttribute(NameOID.USER_ID, u"example"),
        # x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"), 
        # x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Maryland"),
        # x509.NameAttribute(NameOID.LOCALITY_NAME, u"Baltimore"), 
        # x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Opencord"),
        # x509.NameAttribute(NameOID.COMMON_NAME, u"opencord.chat"), 
    ])).add_extension(
        x509.SubjectAlternativeName([
            # Describe what sites we want this certificate for 
            # x509.DNSName(u"opencord.chat"), 
            # x509.DNSName(u"www.opencord.chat")
        ]),
        critical=False,
    ).sign(key, hashes.SHA256())

    # Write our CSR out to disk
    with open('finalcsr.pem', 'wb') as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))


def signKey():
    pass


def get_ip_address_from_san(san_extension):
    for general_name in san_extension.value:
        if isinstance(general_name, IPAddress):
            return general_name.value
    return None


"""
# cert = path to the certificate file
# public_key = Path to public key file 
# private key = Path to the private key file
# password = password for the private key encryption 
"""


def verify(cert=None, public_key=None):
    # Load the third parties public key this
    # file = open("./public_tp.pem", 'rb')

    # Load certificate
    file = open(cert, 'rb')
    cert = x509.load_pem_x509_certificate(file.read())

    if public_key == None:
        tp_path = "public.pem"
    else:
        tp_path = public_key
    public_key_tp = loadKeys(public_key=tp_path)[0]
    # file = open(tp_path, 'rb')
    # tp_cert = x509.load_pem_x509_certificate(file.read())
    # tp_public_key =
    # ca_public_key = serialization.load_pem_public_key(
    #     ca_key_file.read(),
    #     backend=default_backend()
    # )

    # Verify if the certificate is signed by the specified CA
    # This ensures that the specified CA actually used their private key
    try:
        public_key_tp.verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            padding.PKCS1v15(),
            cert.signature_hash_algorithm,
        )
        print("Certificate is signed by the specified third party (CA).")
    except Exception as e:
        print(f"Certificate signature verification failed signature doesn't match public key.")
        # return "Error: Not signed by a valid CA."
        return 1  # return value of 1 means the cert signature is incorrect

    # Get the public key from the certificate

    public_key = cert.public_key()

    # Verify the certificate signature using the certs public key (even self signed certs should pass this)
    try:
        public_key.verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            padding.PKCS1v15(),
            cert.signature_hash_algorithm,
        )
        print("Certificate signature is valid.")
    except Exception as e:
        print(f"Certificate signature verification failed bad signature. ")
        # return "Error: Public key doesn't match the signature."
        return 1

    return 0


def loadCert(cert_path):
    file = open(cert_path, 'rb')
    cert = x509.load_pem_x509_certificate(file.read())

    # verify(cert)
    # common_name = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
    # organization = cert.subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value
    uid = cert.subject.get_attributes_for_oid(NameOID.USER_ID)[0].value
    common_name = cert.issuer.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
    organization = cert.issuer.get_attributes_for_oid(x509.NameOID.ORGANIZATION_NAME)[0].value
    # country = issuer.get_attributes_for_oid(x509.NameOID.COUNTRY_NAME)[0].value 

    # print(f"UUID: {uuid.uuid4()}")
    # print(f"Cert: {cert.issuer}")
    print(f"Issuer Common Name: {common_name}")
    print(f"Issuer Organization: {organization}")
    print(f"Serial number: {cert.serial_number}")
    print(f"Public key: {cert.public_key()}")
    # print(f"Subject: {cert.subject}")
    # print(f"Subject Common Name: {common_name}")
    # print(f"Subject Organization: {organization}")
    print(f"Subject UID: {uid}")
    print(f"Validity Period (before): {cert.not_valid_before}")
    print(f"Validity Period (after): {cert.not_valid_after}")
    print(f"Signature algorithm: {cert.signature_algorithm_oid}")
    # print(f"Subject alternative name: {cert.extensions}")
    san_extension = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
    san_values = san_extension.value
    for name in san_values:
        for general_name in san_extension.value:
            if (isinstance(general_name, IPAddress)):
                print(f"Subject alternative name: {general_name.value}")

    return (cert.serial_number, uid, cert.not_valid_before, cert.not_valid_after)


if __name__ == '__main__':
    generatePEM()
    generateCert()
    loadCert("finalcert.pem")
